import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from .glob_colors import*
from .displayStandards import saveFig
from matplotlib.widgets import RectangleSelector


###########################################################################
# Class : event Handler generic
class eventHandler:
    def __init__(self,fig,ax,path='./',name=''):
        self.cid  = fig.canvas.mpl_connect('key_press_event', self)
        self.fig  = fig
        self.ax   = ax
        self.RS = RectangleSelector(
            ax, self.line_select_callback, drawtype='box', useblit=True,
            button=[1, 3],spancoords='pixels', minspanx=20,minspany=20 )
        self.path,self.name = path,name
        self.selectBox = [0.0,0.0,0.0,0.0]
        self.params = {'paramTest':[0,1]}
        plt.rcParams['keymap.save'] = ''
    
    def __call__(self, event):
        #print ('key entered: ' + key)
        if event.key=='s':
            self.save()
        if event.key=='l':
            self.load()
        if event.key == '0':
            self.action0()
        if event.key in ['1','2','3','4','5','6','7','8','9']:
            self.displayAx(int(event.key))
        if event.key == 'enter':
            self.returnAction()
        if event.key == 'backspace':
            self.backspaceAction()
        if event.key == ' ':
            self.spaceAction()
        if event.key in ['up','right','left','down']:
            self.arrowActions(event.key)
        if event.key in ['a','q']:
            self.activateBox(event.key)
        if event.key in 'zertyuiopdfghjkmwxcvbn':
            self.keyCallBack(event.key)
        self.update()
        
    #can be overriden
    def save(self):
        saveFig(self.path+self.name, self.ax,fmt='png')
    def load(self):
        print('Base load ')
    def update(self):
        print('Base update')
    
    def keyCallBack(self,key):
        print(key)
    def activateBox(self,key):
        if key == 'q':
            self.activateRS(0)
        if key == 'a':
            self.activateRS(1)
    def activateRS(self,b):
        if b==0:
            print(' RectangleSelector deactivated.')
            self.RS.set_active(False)
        if b==1:
            print(' RectangleSelector activated.')
            self.RS.set_active(True)
            
    def line_select_callback(self,eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.selectBox = [x1,x2,y1,y2] 
        print(self.selectBox)

    def displayAx(self,i):
        print('base display ' + str(i))
    def action0(self):
        print('base action0')
    def returnAction(self):
        print('base returnAction')
    def backspaceAction(self):
        print('base backspaceAction')
    def spaceAction(self):
        print('base spaceAction')
    def arrowActions(self,key):
        print('base arrowAction ' + key)
        
def arrowActionsParam(v,dv,key):
    if key == 'up':
        v = v+dv
    if key == 'down':
        v = v-dv
        v = max(v,dv)
    if key == 'right':
        dv = 2*dv
    if key == 'left':
        dv = 0.5*dv
    return v,dv


###########################################################################
#Tests
###########################################################################
def testHandler():
    fig,ax = plt.subplots()
    x = np.linspace(0,1,100)
    ax.plot(x,x)
    ehd=eventHandler(fig,ax,path='/tmp/',name='test')
    plt.show()

if __name__=='__main__':
    #testHandler()
    print(green+__file__.split('/')[-1]+' success'+black)