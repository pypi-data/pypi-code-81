import numpy as np

class ImgData:
    # def __init__(self):
    #     pass

    def loadData(self,filename):
        #TODO to ba implemented
        self.loadFakeData()

    def loadFakeData(self):
        self.x = np.linspace(1,10,100)
        self.y = np.linspace(50,70,500)
        self.z = np.linspace(80,150,250)
        
        # raw data from GG
        self.img = np.random.rand(len(self.x), len(self.y), len(self.z))
        self.img[0,0,0] = np.nan

    
    #xy slice
    def get_slice_parallel(self):
        scale = self.x[1]-self.x[0], self.y[1]-self.y[0]
        pos = self.x[0] - scale[0]/2, self.y[0] - scale[1]/2
        return pos, scale, np.transpose(self.img, (2,0,1))


    # xz slice
    def get_slice_perp(self):
        scale = self.x[1]-self.x[0], self.z[1]-self.z[0]
        pos = self.x[0] - scale[0]/2, self.z[0] - scale[1]/2
        return pos, scale, np.transpose(self.img, (1,0,2))


    #yz slice
    def get_slice_perp2(self):
        scale = self.y[1]-self.y[0], self.z[1]-self.z[0]
        pos = self.y[0] - scale[0]/2, self.z[0] - scale[1]/2
        return pos, scale, np.transpose(self.img, (0,1,2))