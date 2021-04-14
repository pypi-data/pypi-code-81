#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import numpy as np
import cv2
import torch

from img2feat import *

class tests( unittest.TestCase ):
###################################################################
    def suite():
        suite = unittest.TestSuite()
        suite.addTests(unittest.makeSuite(tests))
        return suite
###################################################################

    @classmethod
    def setUpClass(cls): # it is called before test starting
        pass

    @classmethod
    def tearDownClass(cls): # it is called before test ending
        pass

    def setUp(self): # it is called before each test
        pass

    def tearDown(self): # it is called after each test
        pass



###################################################################
    def test_buildnet(self):
        img = torch.rand( (1,3,224,224), dtype=torch.float32 )

#        names = BuildNet.available_names()
        names = ['vgg11', 'resnet18']
        for name in names:
            net, dim_feature = BuildNet.build( name )
            feat = net( img )
            self.assertEqual( feat.shape[0], 1 )
            self.assertEqual( feat.shape[1], dim_feature )
            self.assertEqual( feat.shape[2], 1 )
            self.assertEqual( feat.shape[3], 1 )

###################################################################
    def test_cnn(self):
        img = (np.random.rand( 224, 224, 3 )*255).astype(np.uint8)

#        names = BuildNet.available_names()
        names = ['vgg11', 'resnet18']
        for name in names:
            cnn = CNN( name )
            feat = cnn( [img,img] )
            self.assertEqual( feat.ndim, 2 )
            self.assertEqual( feat.shape[0], 2 )
            self.assertEqual( feat.shape[1], cnn.dim_feature )

###################################################################
    def test_pixelfeature(self):
        img = (np.random.rand( 128, 64, 3 )*255).astype(np.uint8)

#        names = BuildNet.available_names()
        names = ['vgg11']
        for name in names:
            pf = PixelFeature( name )
            f = pf( [img,img] )
            self.assertEqual( len(f), 2 )
            self.assertEqual( f[0].shape[0], img.shape[0] )
            self.assertEqual( f[0].shape[1], img.shape[1] )
            self.assertEqual( f[0].shape[2], pf.dim_feature )


###################################################################
    def test_aug(self):
        img = (np.random.rand( 224, 224, 3 )*255).astype(np.uint8)
        mirror = Mirror()
        aug = mirror( [img] )
        self.assertEqual( len(aug), mirror.nb_aug )
        for a in aug:
            self.assertEqual( a.shape[0], 224 )
            self.assertEqual( a.shape[1], 224 )

        img = (np.random.rand( 480, 640, 3 )*255).astype(np.uint8)
        tencrop = TenCrop( [256] )
        aug = tencrop( [img] )
        self.assertEqual( len(aug), tencrop.nb_aug )
        for a in aug:
            self.assertEqual( a.shape[0], 224 )
            self.assertEqual( a.shape[1], 224 )

###################################################################
    def test_antbee(self):
#        names = BuildNet.available_names()
        names = ['vgg11', 'resnet18']
        for name in names:
            cnn = CNN( name )
            (Xtrain, Ytrain), (Xtest, Ytest) = antbee.load_squared_npy( name )
            self.assertEqual( Ytrain.shape[0], 29+36 )
            self.assertEqual( Xtrain.shape[0], 29+36 )
            self.assertEqual( Xtrain.shape[1], cnn.dim_feature )
            self.assertEqual( Ytest.shape[0], 18+26 )
            self.assertEqual( Xtest.shape[0], 18+26 )
            self.assertEqual( Xtest.shape[1], cnn.dim_feature )

if( __name__ == '__main__' ):
    unittest.main()

