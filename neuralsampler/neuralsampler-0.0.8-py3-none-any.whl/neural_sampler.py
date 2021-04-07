import os

import torch
import torch.optim as optim
from sysflow.utils.common_utils.file_utils import dump, load, make_dir 
import wandb

from neuralsampler.networks import SmallMLP
from neuralsampler.utils import *
from scipy.interpolate import griddata
from tqdm.autonotebook import trange

class neuralsampler: 
    def __init__(self, args, exp_dir, logger): 
        # save the params 
        device = torch.device("cuda:" + str(0) if torch.cuda.is_available() else "cpu")

        #region unpack the params
        niters = args.niters
        batch_size = args.batch_size
        lr = args.lr
        weight_decay = args.weight_decay
        critic_weight_decay = args.critic_weight_decay
        viz_freq = args.viz_freq
        d_iters = args.d_iters
        g_iters = args.g_iters
        l2 = args.l2
        lr_D = args.lr_D
        hid_dim = args.hid_dim
        model = args.model
        dim = args.dim
        G_path = args.G_path
        D_path = args.D_path
        use_spectrum = args.use_spectrum
        clip_D = args.clip_D
        clip_value = args.clip_value
        loss_A = args.loss_A
        mmd_ratio_in = args.mmd_ratio_in
        mmd_two_sample = args.mmd_two_sample
        mmd_beta = args.mmd_beta
        G_loss = args.G_loss
        disc_zero = args.disc_zero
        log_freq = args.log_freq
        max_lr_G = args.max_lr_G
        total_steps_G = args.total_steps_G
        warmup_pct_G = args.warmup_pct_G
        step_decay_factor_G = args.step_decay_factor_G
        step_decay_patience_G = args.step_decay_patience_G
        max_lr_D = args.max_lr_D
        total_steps_D = args.total_steps_D
        warmup_pct_D = args.warmup_pct_D
        step_decay_factor_D = args.step_decay_factor_D
        step_decay_patience_D = args.step_decay_patience_D
        #endregion

        D = SmallMLP(dim, n_hid=hid_dim, n_out=1, UseSpectral=use_spectrum)
        G = SmallMLP(dim, n_hid=hid_dim, n_out=1, UseSpectral=use_spectrum)

        D.to(device)
        G.to(device)

        # load model 
        # pretrained model
        if G_path: 
            G_params = torch.load(G_path)
            G.load_state_dict(G_params)
        if D_path: 
            D_params = torch.load(D_path)
            D.load_state_dict(D_params)

        logger.info(D)
        logger.info(G)

        G_optimizer = optim.Adam(
            G.parameters(), lr=lr, weight_decay=weight_decay, betas=(0.9, 0.999)
        )
        D_optimizer = optim.Adam(
            D.parameters(),
            lr=lr_D,
            betas=(0.9, 0.999),
            weight_decay=critic_weight_decay,
        )

        G_scheduler1 = torch.optim.lr_scheduler.OneCycleLR(
            G_optimizer,
            max_lr=max_lr_G,
            total_steps=total_steps_G, 
            pct_start=warmup_pct_G,  # Warm up for 2% of the total training time
            )

        G_scheduler2 = optim.lr_scheduler.ReduceLROnPlateau(
            G_optimizer, factor=step_decay_factor_G, patience=step_decay_patience_G, verbose=True)

        D_scheduler1 = torch.optim.lr_scheduler.OneCycleLR(
            D_optimizer,
            max_lr=max_lr_D, 
            total_steps=total_steps_D, 
            pct_start=warmup_pct_D,  # Warm up for 2% of the total training time
            )

        D_scheduler2 = optim.lr_scheduler.ReduceLROnPlateau(
            D_optimizer, factor=step_decay_factor_D, patience=step_decay_patience_D, verbose=True)
            
        #region pack the params
        self.device = device
        self.D = D
        self.G = G
        self.G_optimizer = G_optimizer
        self.D_optimizer = D_optimizer
        self.G_scheduler1 = G_scheduler1
        self.G_scheduler2 = G_scheduler2
        self.total_steps_G = total_steps_G
        self.total_steps_D = total_steps_D
        self.D_scheduler1 = D_scheduler1 
        self.D_scheduler2 = D_scheduler2
        self.logger = logger
        self.exp_dir = exp_dir
        self.niters = niters
        self.batch_size = batch_size
        self.lr = lr
        self.weight_decay = weight_decay
        self.critic_weight_decay = critic_weight_decay
        self.viz_freq = viz_freq
        self.d_iters = d_iters
        self.g_iters = g_iters
        self.l2 = l2
        self.lr_D = lr_D
        self.hid_dim = hid_dim
        self.model = model
        self.dim = dim
        self.G_path = G_path
        self.D_path = D_path
        self.use_spectrum = use_spectrum
        self.clip_D = clip_D
        self.clip_value = clip_value
        self.loss_A = loss_A
        self.mmd_ratio_in = mmd_ratio_in
        self.mmd_two_sample = mmd_two_sample
        self.mmd_beta = mmd_beta
        self.G_loss = G_loss
        self.disc_zero = disc_zero
        self.log_freq = log_freq
        #endregion


    def train(self): 

        #region unpack the params
        niters = self.niters
        batch_size = self.batch_size
        viz_freq = self.viz_freq
        d_iters = self.d_iters
        g_iters = self.g_iters
        l2 = self.l2
        model = self.model
        dim = self.dim
        device = self.device
        D = self.D
        G = self.G
        G_optimizer = self.G_optimizer
        D_optimizer = self.D_optimizer
        G_scheduler1 = self.G_scheduler1 
        G_scheduler2 = self.G_scheduler2 
        total_steps_G = self.total_steps_G 
        total_steps_D = self.total_steps_D 
        D_scheduler1 = self.D_scheduler1 
        D_scheduler2 = self.D_scheduler2 
        exp_dir = self.exp_dir
        clip_D = self.clip_D
        clip_value = self.clip_value
        loss_A = self.loss_A
        mmd_ratio_in = self.mmd_ratio_in
        mmd_two_sample = self.mmd_two_sample
        mmd_beta = self.mmd_beta
        G_loss = self.G_loss
        disc_zero = self.disc_zero
        log_freq = self.log_freq
        #endregion

        G.train()
        D.train()


        X_list = []
        Y_list = []
        Z_list = []
        D_list = []

        # get the data via the path (model and dim)
        fname = "{}_d{}.pkl".format(model, dim)
        fname = os.path.join("./dataset/traj", fname)        
        data_dict = load(fname)

        X, Y = data_dict['x'], data_dict['y']

        # trainer the network
        for itr in trange(niters):
            G_optimizer.zero_grad()
            D_optimizer.zero_grad()
            
            #region sample 
            idx = np.random.choice(len(X), batch_size)
            x = X[idx]
            y = Y[idx]
            x = torch.tensor(x, requires_grad=True).float().to(device)
            y = torch.tensor(y, requires_grad=True).float().to(device)

            if mmd_two_sample: 
                idx = np.random.choice(len(X), batch_size)
                x2 = X[idx]
                y2 = Y[idx]
                x2 = torch.tensor(x2, requires_grad=True).float().to(device)
                y2 = torch.tensor(y2, requires_grad=True).float().to(device)
            #endregion

            # 2 gan formulas
            # 2 mmd formula [x8] [combine with the two method] (mmd, mmd_2sample, mmd outside, mmd_2sample outside)

            # loss_A: whether to use the first type of objective
            # ratio_in: whether to put the ratio inside 
            # two_sample: whether to use two pair of samples
            if loss_A:
                # Σ exp(G(xi))/ Z delta_xi, Σ exp(G(xi))/ Z delta_yi
                potential = G(x)
                ratio = torch.exp( potential ) 
                ratio = ratio / ratio.mean()
                D_diff = ratio * ( D(x) - D(y) )
                loss = D_diff.mean()  
                
                if mmd_ratio_in: 
                    # ratio is inside 
                    if mmd_two_sample: 
                        potential2 = G(x2)
                        ratio2 = torch.exp( potential2 ) 
                        ratio2 = ratio2 / ratio2.mean()
                        D_mmd = mmd2(x, y, x2, y2, ratio, ratio2, beta=mmd_beta) 

                    else: 
                        D_mmd = mmd(x, y, ratio, beta=mmd_beta)
                else: 
                    # ratio is outside
                    if mmd_two_sample: 
                        potential = G(x)  
                        potential2 = G(x2) 
                        ratio = torch.exp( potential ) 
                        ratio2 = torch.exp( potential2 ) 
                        D_mmd = mmd2(x, y, x2, y2, ratio, ratio2, beta=mmd_beta) 
                        D_mmd /= ((ratio.mean() + ratio2.mean())/2)**2

                    else:
                        # most likely this will be the same
                        potential = G(x)  
                        ratio = torch.exp( potential ) 
                        D_mmd = mmd(x, y, ratio, beta=mmd_beta) 
                        D_mmd /= (ratio.mean())**2

            else:
                # Σ delta_xi, Σ exp(G(xi)-G(yi))/ Z delta_yi
                potential = G(x) - G(y)
                ratio = torch.exp( potential ) 
                # if 
                # some arguments 
                # ratio = ratio / ratio.mean()
                D_diff = D(x) - D(y) * ratio
                loss = D_diff.mean()  

                if mmd_ratio_in: 
                    if mmd_two_sample: 
                        potential2 = G(x2) - G(y2)
                        ratio2 = torch.exp( potential2 ) 
                        ratio2 = ratio2 / ratio2.mean()
                        D_mmd = mmd2(x, y, x2, y2, torch.ones_like(ratio), ratio, ratio2, beta=mmd_beta)
                    else: 
                        D_mmd = mmd_r2(x, y, torch.ones_like(ratio) , ratio, beta=mmd_beta)

                else: 
                    raise NotImplementedError("hard to move outside: because the importance ratio is not matched in scale: one is one, the other is ratio")

            # lipschitz for Discriminator 
            D_grad = keep_grad(  D(x).sum(), x)

            # two way for the l2 penalty 
            # zero or one 
            if disc_zero: 
                l2_penalty = (D_grad * D_grad).sum(1).mean() * l2  # penalty to enforce f \in F
            else: 
                l2_penalty = ( torch.norm(D_grad, dim=1) -1  ).square().mean() * l2  # penalty to enforce f \in F


            # adversarial training!
            if d_iters > 0 and itr % (g_iters + d_iters) < d_iters : 
                (-1.0 * loss + l2_penalty).backward()
                D_optimizer.step()


                if clip_D: 
                    # Clip weights of discriminator
                    for p in D.parameters():
                        p.data.clamp_(-clip_value, clip_value)
                    
            else:
                if G_loss == 'GAN': 
                    loss.backward()
                elif G_loss == 'MMD': 
                    D_mmd.backward()
                elif G_loss == 'GAN + MMD': 
                    (loss + D_mmd).backward()
                else: 
                    raise NotImplementedError("The loss for the generator of type {} is not implemented".format(G_loss))


                G_optimizer.step()


                if itr < total_steps_G: 
                    G_scheduler1.step()
                else: 
                    G_scheduler2.step(loss)

                if itr < total_steps_D: 
                    D_scheduler1.step()
                else: 
                    D_scheduler2.step(-1.0 * loss + l2_penalty)

            new_dict = { 
                'Discriminator': tc( -1.0 * loss + l2_penalty ), 
                'Generator': tc( loss ), 
                'MMD': tc(D_mmd), 
                'l2 penalty': tc(l2_penalty), 
                'lr_D': D_optimizer.param_groups[0]["lr"],
                'lr_G': G_optimizer.param_groups[0]["lr"], 
            }

            wandb.log(new_dict)

            if itr % viz_freq == 0:
                # figure out the domain for plots 

                if model == 'dw': 
                    # TODO: change this to the init data 
                    x = np.arange(-5.0, 5.0, 0.1)
                    y = np.arange(-5.0, 5.0, 0.1)

                    _X, _Y = np.meshgrid(x, y)
                    z0 = np.concatenate([_X.reshape(-1, 1), _Y.reshape(-1, 1),  np.zeros((_Y.reshape(-1, 1).shape[0], dim -2))], axis=1)
                    # assert dim == 2
                    # need to consider how these goes to high dimension 
                    z0 = torch.tensor(z0, requires_grad=True).float().to(device)

                    potential = G(z0)
                    potential = tc(potential)
                    exp_pot = np.exp( potential )
                    prob = exp_pot / exp_pot.mean()
                    #  Q: do we need to multiple some constant? space volume? 

                    Z = prob.reshape(len(_X), len(_X[0]))

                    critic = D(z0)
                    critic = tc(critic)
                    critic = critic.reshape(len(_X), len(_X[0]))
                    X_list.append(_X)
                    Y_list.append(_Y)
                    Z_list.append(Z)
                    D_list.append(critic)
                    
                elif model == 'mb': 
                    x_list = []
                    y_list = []
                    zi_list = []
                    di_list = []

                    for subfix in ['', '_2', '_3']:
                        x = np.arange(-2, 1, 0.04)
                        y = np.arange(-0.5, 2.5, 0.04)

                        fname = "{}_d{}{}.pkl".format(model, 2, subfix)
                        fname = os.path.join("./dataset/init", fname)
                        x_data = load(fname)
                        z0 = x_data["x"][:2000]

                        xi = x_data['x'][:2000, 0]
                        yi = x_data['x'][:2000, 1]
                    
                        if dim > 2: 
                            z0 = np.concatenate([z0, np.zeros((2000, dim-2))], axis=1)

                        z0 = torch.tensor(z0, requires_grad=True).float().to(device)

                        potential =  G(z0) 
                        potential = tc(potential)
                        exp_pot = np.exp( potential )
                        prob = exp_pot / exp_pot.mean() 
                        zi = griddata((xi, yi), prob, (x[None,:], y[:,None]), method='cubic')

                        critic = D(z0)
                        critic = tc(critic)
                        di = griddata((xi, yi), critic, (x[None,:], y[:,None]), method='cubic')

                        x_list.append(x)
                        y_list.append(y)
                        zi_list.append(zi)
                        di_list.append(di)

                    X_list.append(x_list)
                    Y_list.append(y_list)
                    Z_list.append(zi_list)
                    D_list.append(di_list)
                    
            if itr % log_freq == 0: 
                # log the nn checkpoint 
                model_path = os.path.join(exp_dir, 'model')
                make_dir(model_path)
                torch.save(G.state_dict(), os.path.join(model_path, 'G.pt'))
                torch.save(D.state_dict(), os.path.join(model_path, 'D.pt'))
                
                # log the animation
                new_dict = { 
                    'X': X_list, 
                    'Y': Y_list, 
                    'Z': Z_list, 
                    'D': D_list

                }

                # vis directary
                vis_dir = os.path.join(exp_dir, "vis")
                make_dir(vis_dir)
                fname = "{}_d{}.pkl".format(model, dim)
                dump(new_dict, os.path.join(vis_dir, fname))

        new_dict = { 
            'X': X_list, 
            'Y': Y_list, 
            'Z': Z_list, 
            'D': D_list
        }

        # vis directary
        vis_dir = os.path.join(exp_dir, "vis")
        make_dir(vis_dir)
        fname = "{}_d{}.pkl".format(model, dim)
        dump(new_dict, os.path.join(vis_dir, fname))


