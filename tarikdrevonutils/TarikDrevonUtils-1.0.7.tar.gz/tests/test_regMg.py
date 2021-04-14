from utils import*
import importlib as imp
#imp.reload(matMg)
imp.reload(regMg)

###############################################################################
# def : Test
###############################################################################
def _test_set_regions():
    x = np.linspace(0,1,10)
    reg_lims = [0,0.5,0.8,1.0]
    mats     = ['GaAs','AlAs','GaAs']
    Nds,Nas  = [1e16,0,1e17],[0,1e18,0]
    regs = [regMg.set_region1D(x,reg_lims[i:i+2],mat_name=mats[i],Nd=Nds[i],Na=Nas[i]) for i in range(len(mats))]

    keys = ['Nd','Na','Eg','Xi']
    Nd,Na,Eg,Xi = regMg.set_regions_arrays(x,regs,keys)
    plts = [[x,Nd,'b','$N_d$'],[x,Na,'c','$N_a$'],[x,np.abs(Nd-Na),'m','$N^+$']]
    stddisp(plts,lw=2)
    stddisp([[x,Xi-Eg,'b','$E_g$'],[x,Xi,'c','$\chi$']],lw=2)

if __name__=='__main__':
    plt.close('all')
    _test_set_regions()
