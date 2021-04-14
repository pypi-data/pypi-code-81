from utils import*
import utils.displayStandards as dsp
import importlib as imp
imp.reload(dsp)


def _testStdDispPlt():
    nPts = 10
    x1 = np.linspace(-2,2,nPts);y1 = pow(x1,1)
    x2 = np.linspace(-2,2,nPts);y2 = pow(x2,2)
    x3 = np.linspace(-2,2,nPts);y3 = pow(x3,3)
    plots = [[x1,y1,'r+-.','$x$'  ,1],
             [x2,y2,'gs--','$x^2$',2],
             [x3,y3,'bo--','$x^3$',3]]
    xlabs = ['$x$','$y$']
    stdDispPlt(plots,xlabs, axPos=[0.12, 0.12, 0.8, 0.8], c=['k','b'],
               fonts=[30,25,12,25], texts=[[0.05,0.2,'O','m']])
def _testStdDispPlt_b():
    x = np.linspace(0,1,10)
    plots       = [x,x,'b','x']
    plotsList   = [plots]
    stdDispPlt(plots, showOpt=0)
    stdDispPlt(plotsList)
def _testStdDispPlt_c():
    x = np.linspace(0,1,10)
    plots       = [x,x,[(1.0,0.5,0.2),'s-.'],'x']
    stdDispPlt(plots, showOpt=1)
def _testStdDispPlt_subplots():
    fig,ax = plt.subplots(nrows=1,ncols=2)
    x = np.linspace(0,1,10)
    stdDispPlt([x,2*x,'b','$y1$'],['$x$','$y$'], ax=ax[0],axPos=11, showOpt=0)
    stdDispPlt([x,4*x,'r','$y2$'],['$t$','$y$'], ax=ax[1],axPos=12, showOpt=1,fullsize=True)

def _testAddyAxis():
    nPts = 10
    x1   = np.linspace(-2,2,nPts);y1 = pow(x1,1)
    plotsAx1 = [x1,+y1,'r' ,'']
    plotsAx2 = [x1,-y1,'b','']
    fig,ax = stdDispPlt(plotsAx1,['$x$','$y$'],c=['k','r'],legOpt=0,showOpt=0)
    addyAxis(fig,ax,plotsAx2,'$-y$',c='b', legOpt=0, showOpt=1)
def _testAddxAxis():
    x1 = np.linspace(-2,2,100);y1 = pow(x1,2)
    x2 = np.linspace(-1,1,100);y2 = pow(x2,2)
    plotsAx1 = [x1,y1,'r' ,'$x^2$']
    plotsAx2 = [x2,y2,'b' ,'$x^2$']
    fig,ax = stdDispPlt(plotsAx1,['$x$','$y$'],c=['k','k'],legOpt=0,showOpt=0)
    addxAxis(ax,plotsAx2,'$x_2$',c='b', showOpt=1)

def _testChangeAxLim():
    fig,ax = plt.subplots();plt.plot(range(5),range(5))
    print(changeAxesLim(ax,0.05,xylims=[]))
    print(changeAxesLim(ax,0.05,xylims=[0,1.,0,2.]))
    print(changeAxesLim(ax,0.05,xylims=['x',0,1.]))
    print(changeAxesLim(ax,0.05,xylims=['y',0,2.]))
def _test_get_axPos():
    cmd ='get_axPos(1)' ; print('%-20s: axPos=%s' %(cmd,str(eval(cmd))))
    cmd ='get_axPos(11)'; print('%-20s: axPos=%s' %(cmd,str(eval(cmd))))
    cmd ='get_axPos(21)'; print('%-20s: axPos=%s' %(cmd,str(eval(cmd))))
    cmd ='get_axPos(0)' ; print('%-20s: axPos=%s' %(cmd,str(eval(cmd))))
    cmd ='get_axPos([])'; print('%-20s: axPos=%s' %(cmd,str(eval(cmd))))
    cmd ='get_axPos([0.1, 0])'; print('%-20s: axPos=%s' %(cmd,str(eval(cmd))))
    cmd ='get_axPos([0.1, 0.1, 0.8, 0.8])'; print('%-20s: axPos=%s' %(cmd,str(eval(cmd))))
    cmd ='get_axPos((0.1, 0.1, 0.8, 0.8))'; print('%-20s: axPos=%s' %(cmd,str(eval(cmd))))
def _testGetSymCurve():
    x = np.linspace(0,np.pi,100)
    x1,x2 = x,x
    y1,y2 = np.cos(x1),np.sin(x2)
    x1,y1 = getSymCurve(x1,y1,1)
    x2,y2 = getSymCurve(x2,y2,-1)
    stdDispPlt([[x1,y1,'b','$cos$'],[x2,y2,'r','$sin$']])
def _testGetCML(s):
    c,m,l = getCML(s)
    print('color, marker, linestyle')
    print(c,m,l)
def _test_scat() :
    x,y = np.random.rand(2,10)
    c   = ['b']*10
    s   = [5]*10
    ct  = [(0.2,0.3,0.1)]*10
    stddisp(scat=[x,y,s,c]          ,opt='q',legOpt=0)
    stddisp(scat=[x,y,s[0],c[0]]    ,opt='q',legOpt=0)
    stddisp(scat=[x,y,c]            ,opt='q',legOpt=0)
    stddisp(scat=[x,y,np.array(c)]  ,opt='q',legOpt=0)
    stddisp(scat=[x,y,ct]           ,opt='q',legOpt=0)
    stddisp(scat=[x,y,ct[0]]        ,opt='p',legOpt=0)
def _test_stddisp():
    nPts = 10
    x1 = np.linspace(-2,2,nPts);y1 = pow(x1,1)
    x2 = np.linspace(-2,2,nPts);y2 = pow(x2,2)
    x3 = np.linspace(-2,2,nPts);y3 = pow(x3,3)
    plots = [[x1,y1,'r+-.','$x$'  ,1],
             [x2,y2,'gs--','$x^2$',2],
             [x3,y3,'bo--','$x^3$',3]]
    pol=matplotlib.patches.Polygon([[0,0],[0,1],[1,1]],label='$pol$')
    coll = matplotlib.collections.PatchCollection([pol],'y',alpha=0.3,linewidth=2,edgecolor='g')
    stddisp(plots=plots,colls=[coll],scat=[x1,y1,10,'b'],
            texts=[[0.05,0.2,'This is text','m']],
            labs=['$x$','$y$'], c=['k','b'],pad=2,
            fonts={'text':30,'title':15,'lab':15,'tick':10,'leg':'20'},
            legElt=[pol],opt='p')



def test_display_solutions():
    disp_d = {
        'x1':('get_x1','b',r'$x_1$'),
        'x2':('get_x2','c',r'$x_2$'),
        'y1':('get_y1','r',r'$y_1$'),
        'y2':('get_y2','m',r'$y_2$'),
        }
    class C1:
        def get_x1(self):return np.linspace(0,1,10)
        def get_x2(self):return np.linspace(0,2,10)
        def get_y1(self):return 1*self.get_x1()
        def get_y2(self):return 2*self.get_x2()
    class C2:
        def get_x1(self):return np.linspace(0,1.5,20)
        def get_x2(self):return np.linspace(0,3.0,20)
        def get_y1(self):return 0.5*self.get_x1()
        def get_y2(self):return 3*self.get_x2()
    c1,c2 = C1(),C2()
    objs=[(c1,'ko','$c_1$'), (c2,'ks','$c_2$')]

    dsp.display_solutions(disp_d,objs,key_pair=('x1','y1'),help=0,lw=2)
    dsp.display_solutions(disp_d,objs,key_pair=('x2',['y1','y2']),help=0,lw=2)

if __name__=='__main__':
    plt.close('all')
    #_testGetCML('b:.<')
    #_testStdDispPlt()
    #_testStdDispPlt_b()
    #_testStdDispPlt_c()
    #_testStdDispPlt_subplots()
    #_testAddxAxis()
    #_testAddyAxis()
    #_testChangeAxLim()
    #_testGetSymCurve()
    #_test_get_axPos()
    #_test_scat()
    #_test_stddisp()
    #print(getCML(np.random.rand(3))
    test_display_solutions()
