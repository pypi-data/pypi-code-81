
import numpy as np

def preprocess(input, package, test=0):
	vocafreq = package["vocafreq"]
	voca = package["voca"]
	labelset = package["labelset"]
	input = np.array(open(input, 'r', encoding='utf-8').read().split("\n"))
	corpus = []
	
	doccount = {}
	for i in input:
		document = {}
		sp = i.split("\t")
		if len(sp) == 0:
			label = 'UNI'
		else:
			label = sp[0]

		document["label"] = label
		if label not in doccount:
			doccount[label] = 0
		doccount[label] += 1
		docname = label+str(doccount[label])
		document["document"] = docname
		sp = sp[1].split(" ")
		while " " in sp:
			sp.remove(" ")
		while "" in sp:
			sp.remove("")
		document["split_sentence"] = sp
		if test==0:
			if label not in labelset:
				labelset.append(label)
			for word in sp:
				if word not in vocafreq:
					vocafreq[word] = 0
				vocafreq[word] += 1
		document["length"] = len(sp)
		corpus.append(document)
	if test == 0 :
		vocafreq = {x:vocafreq[x] for x in vocafreq if vocafreq[x]>5 and vocafreq[x]<2000}
		voca = vocafreq.keys()
	for i in corpus:
		i["split_sentence"] = [x for x in i["split_sentence"] if x in vocafreq]

	package["vocafreq"] = vocafreq
	package["voca"] = voca
	package["labelset"] = labelset
	return corpus
