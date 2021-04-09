
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import math
import numpy as np

def tf_ig(corpus,test,package):
	
	labelset = package ["labelset"]
	weights = package ["weights"]
	doclist = package ["doclist"]
	doclist = dict(doclist)
	dictlist = {}
	doclen = {}
	n = len(corpus)
	worddict = {}

	for i in corpus:
		labell = i["label"]
		docl = i["document"]
		if labell not in doclen:
			doclen[labell] = 0
		doclen[labell] += i["length"]
		for j in i["split_sentence"]:
			# ctlist : label —— doc —— word —— frequency
			if labell not in dictlist:
				dictlist[labell] = {}
			if j not in dictlist[labell]:
				dictlist[labell][j] = 1
			else:
				dictlist[labell][j] += 1

			if test ==0 :
				# doclist : label —— word ——　doc set
				if labell not in doclist:
					doclist[labell] = {}
				if j not in doclist[labell]:
					doclist[labell][j] = set()
				doclist[labell][j].add(docl)

	if test ==0:

		for labell in labelset:
			for word in doclist[labell]:
				if word not in worddict:
					worddict[word] = 0
				worddict[word] += len(doclist[labell][word])

		for labell in labelset:
			weights[labell] = {}
			for word in doclist[labell]:
				a_b = worddict[word]
				a = len(doclist[labell][word])
				b = a_b - a
				c_d = sum([(worddict[x]) for x in worddict.keys() if x!=word])
				c = sum([len(doclist[labell][x]) for x in (doclist[labell]) if x!=word])
				d = c_d - c
				weights[labell][word] = -1.0*( (a+c)*1.0/n )*math.log( (a+c)*1.0/n,2 ) + (a*1.0/n)*math.log( a*1.0/(a+b),2 ) + (c*1.0/n)*math.log( c*1.0/(c+d),2 )

	tf_ig = {}
	for labell in labelset:
		tf_ig[labell] = {}
		for word in dictlist[labell]:
			tf_ig[labell][word] = dictlist[labell][word]*1.0 /  (doclen[labell]*1.0)
			if word in weights[labell]:
				tf_ig[labell][word] *= weights[labell][word]
			else:
				tf_ig[labell][word] *= max([ weights[x][word]  for x in weights if word in weights[x]])
	package ["labelset"] = labelset
	package ["weights"] = weights
	package ["doclist"] = doclist

	return tf_ig
