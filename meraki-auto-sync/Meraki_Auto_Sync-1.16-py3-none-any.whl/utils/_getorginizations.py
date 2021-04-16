from autosync import model


async def getOrginizationsAll(db: object, orgsdb):
	orgs = db.organizations.getOrganizations()
	for org in orgs:
		orgsdbtemp = model.ORGDB(org['id'], org['name'])
		orgsdb[org['id']] = orgsdbtemp


# @timeit.timer
async def getOrginizationsWhiteList(db, org, orgsdb):
	info = db.organizations.getOrganization(org)
	orgsdbtemp = model.ORGDB(info['id'], info['name'])
	orgsdb[info['id']] = orgsdbtemp
