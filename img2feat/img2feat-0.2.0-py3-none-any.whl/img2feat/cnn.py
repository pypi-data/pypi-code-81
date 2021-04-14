import cv2
import numpy as np
import torch

from img2feat import BuildNet

class CNN:
    @classmethod
    def available_networks(cls):
        names = []
        for name in BuildNet.available_names():
            if( not name.endswith( 'p2p' ) ):
                names.append( name )
        return names

    def __init__( self, name='vgg11', gpu=False, img_size=(224,224), batch_size=128 ): # img_size=(width,hegith)
        self.__gpu = gpu
        self.__img_size=img_size
        self.batch_size = batch_size

        if( name.lower() in self.available_networks() ):
            self.__network, self.__dim_feature = BuildNet.build( name.lower() )
        else:
            raise NotImplementedError( '**' + name + '** is not implemented.')

        for p in self.__network.parameters():
            p.requires_grad = False

        if self.__gpu:
            self.__network.cuda()
        self.__network.eval()

    @property
    def img_size( self ):
        return self.__img_size

    @property
    def dim_feature( self ):
        return self.__dim_feature

    def imgs2tensor(self, imgs):
        # This function transfer the image to tensor.
        # imgs is list of img
        # img shape : (width, height, channel)
        # tensor shape : (batch, channel, height, width)
        # cv2 (img):BGR, pytorch(tensor):RGB
        # self.img_size: (width, height)

        nb_imgs = len(imgs)
        img_np = np.zeros( (nb_imgs, 3, self.__img_size[1], self.__img_size[0]), dtype=np.float32 )

        for i, img in zip(range(nb_imgs), imgs):
            _img = cv2.resize( img, self.__img_size )

            # BGR -> RGB and fit to imagenet pre-trained model
            img_np[i,2,:,:] = (_img[:,:,0]/255-0.485)/0.229
            img_np[i,1,:,:] = (_img[:,:,1]/255-0.456)/0.224
            img_np[i,0,:,:] = (_img[:,:,2]/255-0.406)/0.225

        img_tensor = torch.from_numpy( img_np )
        if( self.__gpu ):
            img_tensor = img_tensor.cuda()

        return img_tensor

    def tensor2array(self, tensor):
        if( self.__gpu ):
            array = tensor.data.cpu().numpy()
        else:
            array = tensor.data.numpy()
        return array.squeeze( (2,3) )

    def imgs2feature( self, imgs ):
        tensor_imgs = self.imgs2tensor(imgs)
        tensor_feature = self.__network(tensor_imgs)
        array_feature = self.tensor2array( tensor_feature )
        return array_feature

    def __call__( self, imgs ):
        if( type(imgs) is not list ):
            imgs = [imgs]

        array_feature = np.zeros( (len(imgs), self.dim_feature), dtype=np.float32 )

        N = len(imgs) // self.batch_size
        for i in range(N):
            array_feature[i*self.batch_size:(i+1)*self.batch_size,:] = \
                self.imgs2feature( imgs[i*self.batch_size:(i+1)*self.batch_size] )

        array_feature[N*self.batch_size:,:] = \
            self.imgs2feature( imgs[N*self.batch_size:] )

        return array_feature

class PixelFeature:
    @classmethod
    def available_networks(cls):
        names = []
        for name in BuildNet.available_names():
            if( name.endswith( 'p2p' ) ):
                names.append( name[:-3] )
        return names

    def __init__( self, name='vgg11', gpu=False ):
        self.__gpu = gpu

        if( name.lower() in self.available_networks() ):
            self.__network, self.__dim_feature = BuildNet.build( name.lower()+'p2p' )
        else:
            raise NotImplementedError( '**' + name + '** is not implemented.')

        for p in self.__network.parameters():
            p.requires_grad = False

        if self.__gpu:
            self.__network.cuda()
        self.__network.eval()

    @property
    def dim_feature( self ):
        return self.__dim_feature

    def img2tensor(self, img):
        # This function transfer the image to tensor.
        # imgs is list of img
        # img shape : (width, height, channel)
        # tensor shape : (batch, channel, height, width)
        # cv2 (img):BGR, pytorch(tensor):RGB
        # self.img_size: (width, height)

        img_np = np.zeros( (1, 3, img.shape[0], img.shape[1]), dtype=np.float32 )

        # BGR -> RGB and fit to imagenet pre-trained model
        img_np[0,2,:,:] = (img[:,:,0]/255-0.485)/0.229
        img_np[0,1,:,:] = (img[:,:,1]/255-0.456)/0.224
        img_np[0,0,:,:] = (img[:,:,2]/255-0.406)/0.225

        img_tensor = torch.from_numpy( img_np )
        if( self.__gpu ):
            img_tensor = img_tensor.cuda()

        return img_tensor

    def tensor2array(self, tensor):
        if( self.__gpu ):
            array = tensor.data.cpu().numpy()
        else:
            array = tensor.data.numpy()
        return array.transpose( (0,2,3,1) ).squeeze( 0 )

    def __call__( self, imgs ):
        if( type(imgs) is not list ):
            imgs = [imgs]

        array_features = []
        for img in imgs:
            tensor_imgs = self.img2tensor(img)
            tensor_feature = self.__network(tensor_imgs)
            array_features.append( self.tensor2array( tensor_feature ) )
        return array_features

