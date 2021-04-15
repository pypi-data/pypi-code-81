
# imports.
from classes.config import *
from apps.accounts.user import user
from apps.packages.packages import inc_package_manager

# the packages view.
class Packages(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, "packages/", "packages", website=website, landing_page=True)
	def view(self, request):

		# check authenticated.
		if not user.authenticated:
			return self.render(request, html="accounts/html/signin.html")
		elif not user.activated:
			return self.render(request, html="accounts/html/activate.html", template_data={
				"USER": user.info
			})
		else:

			# filters.
			filters, _ = self.parameters.get(request, {
				"os":"*",
				"price":"*",
			})

			# render.
			return self.render(request, {
				"USER": user.info,
				"PACKAGES":inc_package_manager.list(
					os=filters.os,
					price=filters.price,
				),
			})

		#

# the package view.
class Package(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, "packages/", "package", website=website)
	def view(self, request):

		# check authenticated.
		if not user.authenticated:
			return self.render(request, html="accounts/html/signin.html")
		elif not user.activated:
			return self.render(request, html="accounts/html/activate.html", template_data={
				"USER": user.info
			})
		else:

			# get params.
			parameters, response = self.parameters.get(request, [
				"package",
			])
			if not response.success:
				return self.error(message=response.error, request=request)

			# get package.
			try:
				package = inc_package_manager.list()[parameters.package]
			except KeyError:
				return self.error(message=f"Specified package [{parameters.package}] does not exist.", request=request)

			# render.
			installed, purchased, up_to_date = False, False, False
			response = inc_package_manager.installed(parameters.package)
			if response.success: installed = response.installed
			else: print("Error:",response.error)
			response = inc_package_manager.purchased(parameters.package)
			if response.success: purchased = response.purchased
			else: print("Error:",response.error)
			if installed:
				response = inc_package_manager.up_to_date(parameters.package)
				if response.success: up_to_date = response.up_to_date
				else: print("Error:",response.error)
			for key in ["category"]: package[key] = String(package[key]).capitalized_scentence()
			return self.render(request, {
				"OS":dev0s.defaults.vars.os,
				"USER": user.info,
				"PACKAGE":Dictionary(package)+{
					"purchased":purchased,
					"installed":installed,
					"up_to_date":up_to_date,
				},
			})

		#

# the package view.
class Docs(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, "packages/", "docs", website=website, except_xframe=True)
	def view(self, request):

		# check authenticated.
		if not user.authenticated:
			return self.render(request, html="accounts/html/signin.html")
		elif not user.activated:
			return self.render(request, html="accounts/html/activate.html", template_data={
				"USER": user.info
			})
		else:

			# get params.
			parameters, response = self.parameters.get(request, [
				"package",
			])
			if not response.success:
				return self.error(message=response.error, request=request)

			# get package.
			try:
				package = inc_package_manager.list()[parameters.package]
			except KeyError:
				return self.error(message=f"Specified package [{parameters.package}] does not exist.", request=request)

			# render.
			return self.render(request, {
				"USER": user.info,
				"PACKAGE":Dictionary(package)+{
				},
			})

		#

# the package view.
class Purchase(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, "packages/", "purchase", website=website, except_xframe=True)
	def view(self, request):

		# check authenticated.
		if not user.authenticated:
			return self.render(request, html="accounts/html/signin.html")
		elif not user.activated:
			return self.render(request, html="accounts/html/activate.html", template_data={
				"USER": user.info
			})
		else:

			# get params.
			parameters, response = self.parameters.get(request, [
				"package",
			])
			if not response.success:
				return self.error(message=response.error, request=request)

			# get package.
			try:
				package = inc_package_manager.list()[parameters.package]
			except KeyError:
				return self.error(message=f"Specified package [{parameters.package}] does not exist.", request=request)

			# render.
			return self.render(request, {
				"USER": Dictionary(user.info)+{
					"api_key":user.api_key
				},
				"PACKAGE":Dictionary(package)+{
				},
			})

		#

# url patterns.
urlpatterns = w3bsite.views.build_urls([
	Packages(),
	Package(),
	Docs(),
	Purchase(),
])