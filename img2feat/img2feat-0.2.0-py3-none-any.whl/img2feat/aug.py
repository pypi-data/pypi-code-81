# https://blog.shikoan.com/imagenet-preprocessing/

import cv2
import numpy as np

class Mirror:
    def __init__( self ):
        pass

    @property
    def nb_aug( self ):
        return 2

    def __call__( self, imgs ):
        if( type(imgs) is not list ):
            imgs = [imgs]
        aug = []
        for img in imgs:
            aug.append( img )
            aug.append( np.fliplr( img ) )
        return aug

class TenCrop:
    def __init__( self, scales=[224, 256, 384, 480, 640], mirror=True, img_size=(224,224) ): # img_size=(width,height)
        self.scales = scales
        self.mirror = mirror
        self.__img_size = img_size

    @property
    def img_size( self ):
        return self.__img_size

    @property
    def nb_aug( self ):
        r = len(self.scales)*5
        if( self.mirror ):
            r *= 2
        return r

    def __call__( self, imgs ):
        if( type(imgs) is not list ):
            imgs = [imgs]
        aug = []
        for img in imgs:
            for scale in self.scales:
                if( img.shape[0] < img.shape[1] ): # height < width
                    h = scale
                    w = int(img.shape[1] * scale / img.shape[0])
                else:
                    h = int(img.shape[0] * scale / img.shape[1])
                    w = scale
                _img = cv2.resize( img, (w,h) )
                # center
                h0 = int(_img.shape[0] / 2 - self.img_size[1]/2)
                h1 = h0 + self.img_size[1]
                w0 = int(_img.shape[1] / 2 - self.img_size[0]/2)
                w1 = w0 + self.img_size[0]
                aug.append( _img[h0:h1, w0:w1, :] )
                # top left
                aug.append( _img[:self.img_size[1], :self.img_size[0], :] )
                # top right
                aug.append( _img[:self.img_size[1], -self.img_size[0]:, :] )
                # bottom left
                aug.append( _img[-self.img_size[1]:, :self.img_size[0], :] )
                # bottom right
                aug.append( _img[-self.img_size[1]:, -self.img_size[0]:, :] )

                if( self.mirror ):
                    # center
                    aug.append( np.fliplr( _img[h0:h1, w0:w1, :] ) )
                    # top left
                    aug.append( np.fliplr( _img[:self.img_size[1], :self.img_size[0], :] ) )
                    # top right
                    aug.append( np.fliplr( _img[:self.img_size[1], -self.img_size[0]:, :] ) )
                    # bottom left
                    aug.append( np.fliplr( _img[-self.img_size[1]:, :self.img_size[0], :] ) )
                    # bottom right
                    aug.append( np.fliplr( _img[-self.img_size[1]:, -self.img_size[0]:, :] ) )

        return aug

if( __name__ == '__main__' ):
    from scipy import misc
    face = misc.face()
    print( face.shape )

    cv2.imwrite( 'face.png', face )

    tencrop = TenCrop( [256] )
    aug = tencrop( [face] )
    for i, a in zip(range(len(aug)),aug):
        cv2.imwrite( '{}.png'.format(i), a )
