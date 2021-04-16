from autosync import lib
from meraki.exceptions import AsyncAPIError
from .ReSync import reSYNC



async def clone(network, master, appcfg, db, net_id, netName, product,oFunc):
	merakiFunction = getattr(db,product)
	tasks = master.settings()
	for task in tasks:
		if task in oFunc:
			try:
				await eval(
					f"network.Update_{task}( master,appcfg,db,net_id,task,netName)")
			except Exception as e:
				print(f'{lib.bc.FAIL} Network: {netName} ')
				print(f'\t\t - {lib.bc.WARNING}Override for {product} Task: {task} failed with Error {e}{lib.bc.Default}')
		else:
			masterSetting = getattr(master, task)
			networkSetting = getattr(network, task)
			if not await lib.compare(masterSetting, networkSetting):
				print(
					f'\t {lib.bc.OKGREEN}-Updating {task}...{lib.bc.ENDC}')
				if appcfg.WRITE:
					configure = getattr(merakiFunction, f"update{task}")
					try:
						await configure(net_id, **masterSetting)
						await  reSYNC(merakiFunction, net_id, network, task,
									  product,appcfg)
					except AsyncAPIError as e:
						print(
							f'\t {lib.bc.FAIL} Error Running Setting {task} Error Message: {str(e)}  {lib.bc.Default}')
					appcfg.CLEAN = True
					network.ReSync = False
				else:
					print(f"Write Disabled")
			else:
				print(f'\t{lib.bc.OKBLUE} {netName} {lib.bc.OKGREEN}-Settings for  {task} Matched Master{lib.bc.ENDC}')
