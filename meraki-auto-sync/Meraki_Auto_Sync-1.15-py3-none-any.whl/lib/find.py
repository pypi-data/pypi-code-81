
async def idFromName (listDicts, name):
	for ld in listDicts:
		if ld['name'] == name:
			return ld  # ld['groupPolicyId']
	return None


# returns object in list where "name" matches <name>
async def matchGidByName(listDicts, gpid):
	for ld in listDicts:
		if 'groupPolicyId' in ld and ld['groupPolicyId'] == gpid:
			return ld
	return None