
def setDict(dictionary,keys,value):
	dic = dictionary
	for i in range(len(keys)-1):
		if keys[i] not in dic:
			dic[keys[i]] = {}
		dic = dic[keys[i]]
	dic[keys[-1]] = value
	pass

def getDict(dictionary,keys):
	dic = dictionary
	for key in keys:
		if key in dic:
			dic = dic[key]
		else:
			return None
	return dic

def testDict():
	dictionary = {}
	keys = ['config','test','111']
	setDict(dictionary,keys,111)
	print(dictionary)
	print(getDict(dictionary,keys))

if __name__ == '__main__':
	testDict()
