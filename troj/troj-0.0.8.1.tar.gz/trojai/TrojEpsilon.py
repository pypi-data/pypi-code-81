from art.attacks.evasion import *
from .array_utils import *


class TrojEpsAttack:
    def __init__(
        self,
        model,
        learning_rate=0.01,
        eps_steps=0.05,
        max_halving=10,
        max_doubling=10,
        num_iters=15,
        batch_size=128,
        norm=np.inf,
        k=5,
    ):
        self.model = model
        self.budgets = np.arange(0.1, 1, 0.05)
        self.learning_rate = learning_rate
        self.eps_steps = eps_steps
        self.max_halving = max_halving
        self.max_doubling = max_doubling
        self.num_iters = num_iters
        self.batch_size = batch_size
        self.norm = norm
        self.k = k

        attack_dict = {}
        for i in range(self.budgets.shape[0]):
            cw_name = "cw_{}".format(i)
            fgm_name = "fgsm_{}".format(i)
            pgd_name = "pgd_{}".format(i)

            attack_dict[fgm_name] = FastGradientMethod(
                self.model,
                norm=self.norm,
                eps=self.budgets[i],
                eps_step=self.eps_steps,
                batch_size=self.batch_size,
            )
            """
            attack_dict[cw_name] = CarliniLInfMethod(self.model,
                                            learning_rate=self.learning_rate, max_iter=self.num_iters,
                                            max_halving=self.max_halving, max_doubling=self.max_doubling,
                                            eps=self.budgets[i], batch_size=self.batch_size, verbose=False)

            attack_dict[pgd_name] = ProjectedGradientDescent(self.model, norm=self.norm, eps=self.budgets[i],
                                                       eps_step=self.eps_steps,
                                                       batch_size=self.batch_size, max_iter=self.num_iters, verbose=False)
            """
        self.attack_dict = attack_dict

    def generate(self, x, y):
        """
        :param x: inputs
        :param y: labels, either true labels or original unperturbed model labels. y might need to be expanded along
        the first dimension because of art bug.
        :return: adversarial examples
        """
        if len(y.shape) == 1:
            y = np.expand_dims(y, axis=1)
        generated_examples = []
        model_adv_losses = []
        for attacker in list(self.attack_dict.values()):
            adv_x = attacker.generate(x, y)
            if len(y.shape) == 1:
                adv_losses = self.model.loss(
                    adv_x, np.expand_dims(y, axis=1), reduction="none"
                )
            else:
                adv_losses = self.model.loss(adv_x, y, reduction="none")
            model_adv_losses.append(adv_losses)
            generated_examples.append(adv_x)

        generated_examples = np.stack(generated_examples)
        generated_examples = np.swapaxes(generated_examples, 0, 1)

        model_adv_losses = np.stack(model_adv_losses)
        model_adv_losses = np.swapaxes(model_adv_losses, 0, 1)

        high_loss_examples = AdvLossSort(generated_examples, model_adv_losses, k=self.k)
        output = get_min_pert(x, high_loss_examples, norm=self.norm)

        return output
