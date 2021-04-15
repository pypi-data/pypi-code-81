
# classes imports.
from classes.config import *
from apps.packages.packages import inc_package_manager

# install package.
class Install(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/packages/", "install", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"package",])
		if not response.success: return response

		# requests.
		return inc_package_manager.install(parameters.package)
		
		#

# uninstall package.
class Uninstall(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/packages/", "uninstall", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"package",])
		if not response.success: return response

		# requests.
		return inc_package_manager.uninstall(parameters.package)
		
		#

# retrieve the package version.
class Version(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/packages/", "version", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"package"])
		if not response.success: return response
		optional_parameters, _ = self.parameters.get(request, {
			"remote":True,
		})

		# requests.
		return inc_package_manager.version(parameters.package, remote=optional_parameters.remote)
		
		#

# update package.
class Update(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/packages/", "update", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"package",])
		if not response.success: return response

		# requests.
		return inc_package_manager.update(parameters.package)
		
		#


# url patterns.
urlpatterns = w3bsite.views.build_urls([
	Install(),
	Uninstall(),
	Version(),
	Update()
])

#