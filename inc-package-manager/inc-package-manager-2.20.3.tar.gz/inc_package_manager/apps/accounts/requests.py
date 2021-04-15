
# classes imports.
from classes.config import *
from apps.accounts.user import user
from apps.packages.packages import inc_package_manager

# sign in.
class SignIn(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/accounts/", "signin", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"username",
			"password",])
		if not response.success: return response

		# requests.
		response = user.signin(
			username=parameters.username,
			password=parameters.password,
		)
		if response.success:
			_response_ = inc_package_manager.connect()
			if not _response_.success: return _response_
		return response
		
		#

# sign in.
class SignOut(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/accounts/", "signout", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		return user.signout()
		
		#

# sign up.
class SignUp(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/accounts/", "signup", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"username",
			"email",
			"name",
			"password",
			"verify_password",
			#"code",
		])
		if not response.success: return response

		# requests.
		return user.signup(
			username=parameters.username,
			email=parameters.email,
			name=parameters.name,
			password=parameters.password,
			verify_password=parameters.verify_password,
			#code=parameters.code,
		)
		
		#

# request a reset password verification code.
class SendCode(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/accounts/", "send_code", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"username",
			"mode",])
		if not response.success: return response

		# requests.
		return user.send_code(
			username=parameters.username,
			mode=parameters.mode,
		)
		
		#

# reset the user's password.
class ResetPassword(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/accounts/", "reset_password", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"username",
			"code",
			"password",
			"verify_password",])
		if not response.success: return response

		# requests.
		return user.reset_password(
			username=parameters.username,
			code=parameters.code,
			password=parameters.password,
			verify_password=parameters.verify_password,
		)
		
		#

# activate a newly created user.
class Activate(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/accounts/", "activate", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"code",])
		if not response.success: return response

		# check authenticated.
		if not user.authenticated:
			return self.error("The current user is not authenticated.")

		# requests.
		return user.activate(
			code=parameters.code,
		)
		
		#
# edit user.
class Edit(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/accounts/", "edit", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"email",
			"name",])
		if not response.success: return response

		# check authenticated.
		if not user.authenticated:
			return self.error("The current user is not authenticated.")

		# requests.
		return user.edit(
			email=parameters.email,
			name=parameters.name,
		)
		
		#

# edit the user's password.
class EditPassword(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			"requests/accounts/", "edit_password", 
			website=website,
			auth_required=False, 
			root_required=False, )
	def request(self, request):
		
		# check authenicated.
		parameters, response = self.parameters.get(request, [
			"password",
			"new_password",
			"verify_password",])
		if not response.success: return response

		# check authenticated.
		if not user.authenticated:
			return self.error("The current user is not authenticated.")

		# requests.
		return user.edit_password(
			password=parameters.password,
			new_password=parameters.new_password,
			verify_password=parameters.verify_password,
		)
		
		#

# url patterns.
urlpatterns = w3bsite.views.build_urls([
	SignIn(),
	SignUp(),
	SignOut(),
	SendCode(),
	ResetPassword(),
	Activate(),
	Edit(),
	EditPassword(),
])

#