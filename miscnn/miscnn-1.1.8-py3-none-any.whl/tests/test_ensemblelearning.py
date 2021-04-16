#==============================================================================#
#  Author:       Dominik Müller                                                #
#  Copyright:    2020 IT-Infrastructure for Translational Medical Research,    #
#                University of Augsburg                                        #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#==============================================================================#
#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
#External libraries
import unittest
import tempfile
import os
import numpy as np
#Internal libraries
from miscnn import Data_IO, Preprocessor, Neural_Network, Data_Augmentation
from miscnn.data_loading.interfaces import Dictionary_interface
from miscnn.neural_network.data_generator import DataGenerator

#-----------------------------------------------------#
#              Unittest: Neural Network               #
#-----------------------------------------------------#
class EnsembleLearningTest(unittest.TestCase):
    # Create random imaging and segmentation data
    @classmethod
    def setUpClass(self):
        np.random.seed(1234)
        # Create 2D imgaging and segmentation data set
        self.dataset2D = dict()
        for i in range(0, 6):
            img = np.random.rand(16, 16) * 255
            self.img = img.astype(int)
            seg = np.random.rand(16, 16) * 3
            self.seg = seg.astype(int)
            self.dataset2D["TEST.sample_" + str(i)] = (self.img, self.seg)
        # Initialize Dictionary IO Interface
        io_interface2D = Dictionary_interface(self.dataset2D, classes=3,
                                              three_dim=False)
        # Initialize temporary directory
        self.tmp_dir2D = tempfile.TemporaryDirectory(prefix="tmp.miscnn.")
        tmp_batches = os.path.join(self.tmp_dir2D.name, "batches")
        # Initialize Data IO
        self.data_io2D = Data_IO(io_interface2D,
                                 input_path=os.path.join(self.tmp_dir2D.name),
                                 output_path=os.path.join(self.tmp_dir2D.name),
                                 batch_path=tmp_batches, delete_batchDir=False)
        # Initialize Data Augmentation
        self.data_aug2D = Data_Augmentation(cycles=1, scaling=True,
                                            rotations=True,
                                            elastic_deform=False,
                                            mirror=False, brightness=True,
                                            contrast=True, gamma=True,
                                            gaussian_noise=True)
        # Initialize Preprocessor
        self.pp2D = Preprocessor(self.data_io2D, batch_size=2,
                                 data_aug=self.data_aug2D, analysis="fullimage")
        # Initialize Neural Network
        self.nn2D = Neural_Network(preprocessor=self.pp2D)
        # Get sample list
        self.sample_list2D = self.data_io2D.get_indiceslist()
        # Create 3D imgaging and segmentation data set
        self.dataset3D = dict()
        for i in range(0, 6):
            img = np.random.rand(16, 16, 16) * 255
            self.img = img.astype(int)
            seg = np.random.rand(16, 16, 16) * 3
            self.seg = seg.astype(int)
            self.dataset3D["TEST.sample_" + str(i)] = (self.img, self.seg)
        # Initialize Dictionary IO Interface
        io_interface3D = Dictionary_interface(self.dataset3D, classes=3,
                                              three_dim=True)
        # Initialize temporary directory
        self.tmp_dir3D = tempfile.TemporaryDirectory(prefix="tmp.miscnn.")
        tmp_batches = os.path.join(self.tmp_dir3D.name, "batches")
        # Initialize Data IO
        self.data_io3D = Data_IO(io_interface3D,
                                 input_path=os.path.join(self.tmp_dir3D.name),
                                 output_path=os.path.join(self.tmp_dir3D.name),
                                 batch_path=tmp_batches, delete_batchDir=False)
        # Initialize Data Augmentation
        self.data_aug3D = Data_Augmentation(cycles=1, scaling=True,
                                            rotations=True,
                                            elastic_deform=False,
                                            mirror=False, brightness=True,
                                            contrast=True, gamma=True,
                                            gaussian_noise=True)
        # Initialize Preprocessor
        self.pp3D = Preprocessor(self.data_io3D, batch_size=2,
                                 data_aug=self.data_aug3D,
                                 analysis="patchwise-grid", patch_shape=(4,4,4))
        # Initialize Neural Network
        self.nn3D = Neural_Network(preprocessor=self.pp3D)
        # Get sample list
        self.sample_list3D = self.data_io3D.get_indiceslist()

    # Delete all temporary files
    @classmethod
    def tearDownClass(self):
        self.tmp_dir2D.cleanup()
        self.tmp_dir3D.cleanup()

    #-------------------------------------------------#
    #              Inference Augmentation             #
    #-------------------------------------------------#
    # Inference Augmentation Test 2D - Basic
    def test_INFERENCEAUG_preprocessing_2D(self):
        self.data_aug2D.infaug = True
        # Initialize Keras Data Generator for generating batches
        dataGen = DataGenerator([self.sample_list2D[0]], self.pp2D,
                                training=False, validation=False,
                                shuffle=False, iterations=None)
        # Run prediction process with Keras predict
        pred_list = []
        for batch in dataGen:
            print("2D")

    # Inference Augmentation Test 3D - Basic
    def test_INFERENCEAUG_preprocessing_3D(self):
        self.data_aug3D.infaug = True
        # Initialize Keras Data Generator for generating batches
        dataGen = DataGenerator([self.sample_list3D[0]], self.pp3D,
                                training=False, validation=False,
                                shuffle=False, iterations=None)
        # Run prediction process with Keras predict
        pred_list = []
        for batch in dataGen:
            print("3D")
