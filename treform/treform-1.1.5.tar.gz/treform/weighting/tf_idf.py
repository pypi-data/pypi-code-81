
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import math

def tf_idf(corpus, test , package):
	
	dictlist = {}
	doclen = {}
	docname = package ["docname"]
	weights = package ["weights"]

	for i in corpus:
		labell = i["label"]
		docl = i["document"]
		doclen[docl] = i["length"]
		for j in i["split_sentence"]:
			# dctlist : doc —— word —— frequency
			if docl not in dictlist:
				dictlist[docl] = {}
			if j not in dictlist[docl]:
				dictlist[docl][j] = 0
			dictlist[docl][j] += 1
			if test==0:
				# doclist :  word ——　doc set
				if j not in weights:
					weights[j] = set()
				weights[j].add(docl)
				docname.add(docl)
	if test ==0:
		for word in weights:
			weights[word] = math.log( ( 1+len(docname)*1.0)/(len(weights[word])*1.0),2)
	tf_idf_weight = {}
	for doc in dictlist:
		tf_idf_weight[doc] = {}
		for word in dictlist[doc]:
			# tf:
			tf_idf_weight[doc][word] = dictlist[doc][word]*1.0 / (doclen[doc]*1.0)
			# tf*idf
			tf_idf_weight[doc][word] *= weights[word]
	package ["docname"] = docname
	package ["weights"] = weights
	#print(tf_idf_weight)
	return tf_idf_weight