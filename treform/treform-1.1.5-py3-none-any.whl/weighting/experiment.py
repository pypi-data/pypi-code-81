
import os
import math
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np
import pandas as pd

from treform.weighting.one_hot import one_hot
from treform.weighting.preprocess import preprocess
from sklearn import preprocessing

from treform.weighting.tf_idf import tf_idf
from treform.weighting.tf_dc import tf_dc
from treform.weighting.tf_bdc import tf_bdc
from treform.weighting.tf_ig import tf_ig
from treform.weighting.tf_eccd import tf_eccd
from treform.weighting.tf_chi import tf_chi
from treform.weighting.tf_rf import tf_rf
from treform.weighting.iqf_qf_icf import iqf_qf_icf

def init(package):
	package["voca"] = []
	package["labelset"] = []
	package["vocafreq"] = {}
	package["weights"] = {}
	package["doclist"] = []
	package["docname"] = set()

def getXY(input, algo, test=0):
	global package
	corpus = preprocess(input, package, test)
	labelset = package["labelset"]
	voca = package["voca"]
	
	level = 2
	mod = 0
	if algo == "tf_idf":
		weights = tf_idf(corpus,test,package)
		print('----------tf-idf--------')
		print(weights)

		mod=1
	elif algo == "tf_dc":
		weights = tf_dc(corpus,test,package)
	elif algo == "tf_bdc":
		weights = tf_bdc(corpus,test,package)
	elif algo == "iqf_qf_icf":
		weights = iqf_qf_icf(corpus,test,package)
		print('----------iqf_qf_icf--------')
		for doc in weights:
			print(weights[doc])

	elif algo == "tf_eccd":
		weights = tf_eccd(corpus,test,package)
	elif algo == "tf_ig":
		weights = tf_ig(corpus,test,package)
	elif algo == "tf_rf":
		weights = tf_rf(corpus,test,package)
		level = 3
	elif algo == "tf_chi":
		weights = tf_chi(corpus,test,package)
		level = 3
	#print weights 
	X = []
	Y = []
	count = 0
	vocalen = len(voca)
	for doc in corpus:
		if count%100 ==0:
			print(str(count) + "/" + str(len(corpus)))
		count+=1
		# process label
		labelset.append(doc["label"])
		Y.append(int(np.argmax(one_hot(labelset)[-1])))
		labelset = labelset[:-1]
		
		# process word
		temvocalist = list(voca) + doc["split_sentence"]
		tem_one_hot = one_hot(temvocalist)[vocalen:]
		for word in range(len(tem_one_hot)):
			temlabel = doc["label"]
			temword = doc["split_sentence"][word]
			temdoc = doc["document"]
			if level == 2:
				if mod ==0:
					tem_one_hot[word] *= weights[temlabel][temword]
				else:
					tem_one_hot[word] *= weights[temdoc][temword]
			else:
				tem_one_hot[word] *= weights[temlabel][temdoc][temword]

	return np.squeeze(X),Y

def main( trainf, algo="tf_idf"):
	global package
	init(package)
	train_x, train_y = getXY(trainf,algo,test=0)

package = {}
trainf = "../../sample_data/Reuters_train.txt"
testf = "../../sample_data/Reuters_test.txt"

#main(testf,algo="tf_idf")
#main(trainf,algo="tf_dc")
#main(trainf,algo="tf_bdc")
main(testf,algo="iqf_qf_icf")
#main(trainf,algo="tf_rf")
#main(trainf,algo="tf_chi")
#main(trainf,algo="tf_eccd")
