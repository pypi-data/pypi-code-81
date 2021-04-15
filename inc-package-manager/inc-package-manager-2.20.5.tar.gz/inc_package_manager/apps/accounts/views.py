
# imports.
from classes.config import *
from apps.accounts.user import user
	
# sign in.
class SignIn(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, f"accounts/", "signin", website=website)
	def view(self, request):
		return self.render(request, {
			"USER":user.info,
		})
class SignInCopy(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, f"accounts/", "login", website=website, html="accounts/html/signin.html")
	def view(self, request):
		return self.render(request, {
			"USER":user.info,
		})

# sign up.
class SignUp(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, f"accounts/", "signup", website=website)
	def view(self, request):
		return self.render(request, {
			"USER":user.info,
		})

# reset password.
class Reset(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, f"accounts/", "reset", website=website)
	def view(self, request):
		return self.render(request, {
			"USER":user.info,
		})

# activate account.
class Activate(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, f"accounts/", "activate", website=website)
	def view(self, request):
		if not user.authenticated:
			return self.render(request, html="accounts/html/signin.html", template_data={
				"USER": user.info
			})
		else:
			return self.render(request, {
				"USER":user.info,
			})

# the updating view.
class Account(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, "accounts/", "account", website=website)
	def view(self, request):
		if not user.authenticated:
			return self.render(request, html="accounts/html/signin.html", template_data={
				"USER": user.info
			})
		elif not user.activated:
			return self.render(request, html="accounts/html/activate.html", template_data={
				"USER": user.info
			})
		else:
			return self.render(request, {
				"USER": user.info
			})

		#

# url patterns.
urlpatterns = w3bsite.views.build_urls([
	SignIn(),
	SignInCopy(),
	SignUp(),
	Reset(),
	Activate(),
	Account(),
])