# same as compare() but strips out ID/networkID for profiles/group policies etc
import copy
async def soft_compare(A, B):
	t_A = copy.deepcopy(A)
	t_B = copy.deepcopy(B)
	if 'id' in t_A: t_A.pop('id')
	if 'networkId' in t_A: t_A.pop('networkId')
	if 'groupPolicyId' in t_A: t_A.pop('groupPolicyId')
	if 'id' in t_B: t_B.pop('id')
	if 'networkId' in t_B: t_B.pop('networkId')
	if 'groupPolicyId' in t_B: t_B.pop('groupPolicyId')
	
	if 'dnsRewrite' in t_A: t_A.pop('dnsRewrite')
	if 'dnsRewrite' in t_B: t_B.pop('dnsRewrite')
	if 'adultContentFilteringEnabled' in t_A: t_A.pop(
		'adultContentFilteringEnabled')
	if 'adultContentFilteringEnabled' in t_B: t_B.pop(
		'adultContentFilteringEnabled')
	
	# had to add some logic to pop the "id" and "radsecEnabled". 'id' is unique and 'radsecEnabled' is beta for openroaming
	if 'radiusServers' in t_A:
		t_A['radiusServers'][0].pop('id')
		if 'radsecEnabled' in t_A['radiusServers'][0]:
			t_A['radiusServers'][0].pop('radsecEnabled')
		
		if 'radiusAccountingServers' in t_A:
			t_A['radiusAccountingServers'][0].pop('id')
			if 'radsecEnabled' in t_A['radiusAccountingServers'][0]:
				t_A['radiusAccountingServers'][0].pop('radsecEnabled')
	if 'radiusServers' in t_B:
		t_B['radiusServers'][0].pop('id')
		if 'radsecEnabled' in t_B['radiusServers'][0]:
			t_B['radiusServers'][0].pop('radsecEnabled')
		
		if 'radiusAccountingServers' in t_B:
			t_B['radiusAccountingServers'][0].pop('id')
			if 'radsecEnabled' in t_B['radiusAccountingServers'][0]:
				t_B['radiusAccountingServers'][0].pop('radsecEnabled')
	
	return await compare(t_A, t_B)


# compares JSON objects, directionarys and unordered lists will be equal
async def compare(A, B):
	result = True
	if A == None and B == None:
		return True
	if not type(A) == type(B):
		# print(f"Wrong type")
		return False
	try:
		if not type(A) == int and not type(A) == bool and not len(
				A) == len(B):
			# print(f'Not the same length')
			return False
	except:
		print()
	
	if type(A) == dict:
		for a in A:
			if a in B and not await compare(A[a], B[a]):
				return False
	elif type(A) == list:
		for a in A:
			if not a in B:
				return False
	else:
		if not A == B:
			return False
	return result
##END-OF COMPARE
