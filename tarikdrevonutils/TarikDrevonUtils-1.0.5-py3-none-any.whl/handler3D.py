from mpl_toolkits.mplot3d import proj3d
import numpy, importlib,sys


def orthogonal_proj(zfront, zback):
    a = (zfront+zback)/(zfront-zback)
    b = -2*(zfront*zback)/(zfront-zback)
    return numpy.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,a,b],
                        [0,0,0,zback]])
# proj3d.persp_transformation = orthogonal_proj
def set_perspective(b=False):
    importlib.reload(proj3d)
    if not b :
        print('setting persp_transformation as orthogonal')
        proj3d.persp_transformation = orthogonal_proj

class handler_3d:
    def __init__(self,fig,e=[1,0,0],persp=False):
        self.dazim=5
        self.delev=5
        self.fig = fig
        self.fig.canvas.mpl_connect('key_press_event', self)
        self.e=e
        set_perspective(b=persp)
    def __call__(self,event):
        #print(event.key)
        ax = event.canvas.figure.axes[0];
        # dx,dy,dz = 0,0,0
        if event.key == '1'     : ax.elev,ax.azim = 0,0
        if event.key == '2'     : ax.elev,ax.azim = 0,90
        if event.key == '3'     : ax.elev,ax.azim = 90,90
        if event.key == '4'     : ax.elev,ax.azim = 180,0
        if event.key == '5'     : ax.elev,ax.azim = 0,-90
        if event.key == '6'     : ax.elev,ax.azim = -90,-90
        if event.key == 'up'    : ax.elev-=self.delev
        if event.key == 'down'  : ax.elev+=self.delev
        if event.key == 'left'  : ax.azim-=self.dazim
        if event.key == 'right' : ax.azim+=self.dazim
        if event.key == 'ctrl+up'   : self.delev+=5
        if event.key == 'ctrl+down' : self.delev = max(5,self.delev-5)
        if event.key == 'ctrl+left' : self.dazim = max(5,self.dazim-5)
        if event.key == 'ctrl+right': self.dazim+=5
        if event.key == 'ctrl+r'    : self.delev,self.dazim=5,5
        if 'ctrl' in event.key :
            print('delev=%d,dazim=%d' %(self.delev,self.dazim))
        else:
            print('elev=%d,azim=%d' %(ax.elev,ax.azim))
        event.canvas.draw()
