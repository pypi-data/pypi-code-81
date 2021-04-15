#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
from dev0s.shortcuts import *
dev0s.defaults.insert(dev0s.defaults.source_path(__file__, back=1))
from classes.config import *
from apps.packages.packages import inc_package_manager
dev0s.system.env["INC_PACKAGE_MANAGER_CLI"] = True

# the cli object class.
class CLI(dev0s.cli.CLI):
	def __init__(self):
		
		# defaults.
		dev0s.cli.CLI.__init__(self,
			modes={
				"--install package-name":"Install a package.",
				"--uninstall package-name":"Uninstall a package.",
				"--update [optional: package-name]":"Update all packages, optionally specify one package to update.",
				"--version package-name [optional: --remote]":"Retrieve the installed / remote version of a package.",
				"--requirements package-name [optional: --remote]":"Retrieve the installed / remote version of a package in requirements format.",
				"--config":f"Configure the {ALIAS}.",
				"   --api-key your-api-key":"Specify your vandenberghinc api key.",
				"-h / --help":"Show the documentation.",
			},
			options={
				"-y / --assume-yes":"Do not prompt for the [Are you sure] warning.",
				"-j / --json":"Print the response in json format.",
				"--log-level <int>":"Overwrite the default log levels.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):

		# check arguments.
		if not self.arguments.present("--w3bsite"):
			self.arguments.check(exceptions=["--log-level", "--create-alias", "--version", "--remote", "--unstable"], json=dev0s.defaults.options.json)

		# help.
		if self.arguments.present(['-h', '--help']):
			self.docs(success=True, json=dev0s.defaults.options.json)

		# config.
		elif self.arguments.present('--config'):
			loader = dev0s.console.Loader(f"Updating the configuration setttings")
			edits = 0
			api_key = self.arguments.get('--api-key', required=False, json=dev0s.defaults.options.json)
			if api_key != None:
				inc_package_manager.configuration.dictionary["api_key"] = api_key
				edits += 1 
			if edits == 0:
				loader.stop()
				os.system(f"nano {inc_package_manager.configuration.fp.path}")
			if edits > 0:
				inc_package_manager.configuration.save()
				loader.stop()
				self.stop(message=f"Successfully saved {edits} edit(s).", json=dev0s.defaults.options.json)
			#else:
			#	loader.stop(success=False)
			#	self.stop(error=f"Speficy one of the configuration arguments to edit. Run ($ {ALIAS} -h) for more info.", json=dev0s.defaults.options.json)

		# w3bsite cli.
		elif self.arguments.present("--w3bsite"):
			website.cli()

		# install a package.
		elif self.arguments.present('--install'):
			c = 0
			for package in self.arguments.get('--install', format=list):
				response = inc_package_manager.install(package, stable=not self.arguments.present("--unstable"))
				if not response.success:
					self.stop(response=response, json=dev0s.defaults.options.json)
				c += 1
			self.stop(message=f"Successfully installed {c} package(s).", json=dev0s.defaults.options.json)

		# uninstall a package.
		elif self.arguments.present('--uninstall'):
			package = self.arguments.get('--uninstall', json=dev0s.defaults.options.json)
			if not self.arguments.present(["-y", "--assume-yes"]) and not dev0s.defaults.options.json and not dev0s.console.input(f"&ORANGE&Warning!&END& You are uninstalling package {_package_}. Do you wish to proceed?", yes_no=True):
				self.stop(message="Aborted.")
			self.stop(response=inc_package_manager.uninstall(package, stable=not self.arguments.present("--unstable")), json=dev0s.defaults.options.json)

		# update a package.
		elif self.arguments.present('--update'):
			package = self.arguments.get('--update', required=False, default="all")
			if package in ["all", "*"]:
				response = inc_package_manager.update("all", stable=not self.arguments.present("--unstable"))
				self.stop(response=response, json=dev0s.defaults.options.json)
			else:
				c = 0
				for package in self.arguments.get('--update', format=list):
					response = inc_package_manager.update(package, stable=not self.arguments.present("--unstable"))
					if not response.success:
						self.stop(response=response, json=dev0s.defaults.options.json)
				self.stop(message=f"Successfully updated {c} package(s).", json=dev0s.defaults.options.json)

		# get the version of a package.
		elif self.arguments.present(['--version', "--requirements"]):
			if self.arguments.present(["--version"]):
				packages = self.arguments.get('--version', format=list, json=dev0s.defaults.options.json)
			else:
				packages = self.arguments.get('--requirements', format=list, json=dev0s.defaults.options.json)
			remote = self.arguments.present("--remote")
			c = 0
			for package in packages:
				response = inc_package_manager.version(package, stable=not self.arguments.present("--unstable"))
				if not response["success"]:
					self.stop(response=response, json=dev0s.defaults.options.json)
				else:
					if self.arguments.present(["--requirements"]):
						dev0s.response.log(f"{package}=={response.version}", json=dev0s.defaults.options.json)
					else:
						dev0s.response.log(f"{package} version: {response.version}", json=dev0s.defaults.options.json)
					c += 1
			if c == 0:
				self.stop(error=f"There are no packages installed.", json=dev0s.defaults.options.json)
			else: sys.exit(1)

		# invalid.
		else: self.invalid(json=dev0s.defaults.options.json)

		#
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
