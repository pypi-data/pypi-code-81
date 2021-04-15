
# imports.
from classes.config import *
from apps.packages.packages import inc_package_manager

# the user object class.
class User(Object):
	def __init__(self):

		# defaults.
		Object.__init__(self)

		# sys attributes.
		self.__username__ = None
		self.__email__ = None
		self.__name__ = None
		self.__api_key__ = None
		self.__password__ = None
		self.__authenticated__ = False
		self.__activated__ = False

		#

	# signup to api.vandenberghinc.com
	def signup(self,
		# the user's username.
		username=None,
		# the user's email.
		email=None,
		# the user's name.
		name=None,
		# the users's password.
		password=None,
		# the users's verify password for signup.
		verify_password=None,
		# the verification code send to the email.
		code=None,
	):

		# check signed in.
		if self.authenticated:
			return dev0s.response.error("The current user is already authenticated.")
			
		# request.
		response = self.__request__("/requests/accounts/signup/", {
			"username":username,
			"email":email,
			"name":name,
			"password":password,
			"verify_password":verify_password,
			"code":code,
		})
		if response.success:
			self.__username__ = username
			self.__email__ = email
			self.__name__ = name
			self.__password__ = password
		return response

		#

	# signin to api.vandenberghinc.com
	def signin(self,
		# the user's username.
		username=None,
		# the users's password.
		password=None,
	):

		# check signed in.
		if self.authenticated:
			return dev0s.response.success("The current user is already authenticated.")
			
		# request.
		response = self.__request__("/requests/accounts/signin/", {
			"username":username,
			"password":password,
		})
		if response.success:
			self.__authenticated__ = True
			self.__activated__ = response.activated
			self.__username__ = username
			self.__password__ = password
			self.__api_key__ = response.api_key
			self.__name__ = response.name
			self.__email__ = response.email
			inc_package_manager.api_key = response.api_key
		return response

		#

	# signout.
	def signout(self,
		# the user's username.
		username=None,
		# the users's password.
		password=None,
	):

		# check signed in.
		if not self.authenticated:
			return dev0s.response.success("The current user is not authenticated.")
			
		# request.
		username = self.username
		self.__username__ = None
		self.__email__ = None
		self.__name__ = None
		self.__api_key__ = None
		self.__password__ = None
		self.__authenticated__ = False
		self.__activated__ = False
		inc_package_manager.api_key = None
		return dev0s.response.success(f"Successfully signed out {username}.")

		#

	# edit the user's settings.
	def edit(self,
		# the new email.
		email=None,
		# the new name.
		name=None,
	):

		# check signed in.
		if not self.authenticated:
			return dev0s.response.error("The current user is not authenticated.")

		# check params.
		if [email,name] == [None,None]:
			return dev0s.response.error("Define one of the following parameters: [email, name].")

		# request.
		response = self.__request__("/requests/accounts/edit/", {
			"email":email,
			"name":name,
		})
		if response.success:
			if email != None: self.__email__ = email
			if name != None: self.__name__ = name
		return response

		#

	# edit the user's password.
	def edit_password(self,
		# the current password (str).
		password=None,
		# the new password (str).
		new_password=None,
		# the verify password (str).
		verify_password=None,
	):

		# check signed in.
		if not self.authenticated:
			return dev0s.response.error("The current user is not authenticated.")

		# check params.
		response = dev0s.response.parameters.check(
			parameters={
				"password:str":password,
				"new_password:str":new_password,
				"verify_password:str":verify_password,
			})
		if not response.success: return response

		# check current.
		if password != self.__password__:
			return dev0s.response.error("Provided an incorrect password.")

		# request.
		response = self.__request__("/requests/accounts/edit_password/", {
			"password":password,
			"new_password":new_password,
			"verify_password":verify_password,
		})
		if response.success:
			self.__password__ = password
		return response

		#

	# send verfication code.
	def send_code(self,
		# the user's username (str).
		username=None,
		# the verification code's mode.
		mode="reset_password",
	):

		# check params.
		response = dev0s.response.parameters.check(
			parameters={
				"username:str":username,
				"mode:str":mode,
			})
		if not response.success: return response

		# request.
		return self.__request__("/requests/accounts/send_code/", {
			"username":username,
			"mode":mode,
		})

		#

	# reset the user's password.
	def reset_password(self,
		# the user's username (str).
		username=None,
		# the verification code send to the email (str).
		code=None,
		# the new password (str).
		password=None,
		# the verify password (str).
		verify_password=None,
	):

		# check signed in.
		if self.authenticated:
			return dev0s.response.error("The current user is already authenticated.")

		# check params.
		response = dev0s.response.parameters.check(
			parameters={
				"username:str":username,
				"code:str":code,
				"password:str":password,
				"verify_password:str":verify_password,
			})
		if not response.success: return response

		# request.
		response = self.__request__("/requests/accounts/reset_password/", {
			"username":username,
			"code":code,
			"password":password,
			"verify_password":verify_password,
		})
		if response.success:
			self.__password__ = password
		return response

		#

	# activate a newly created account.
	def activate(self,
		# the verification code send to the email (str).
		code=None,
	):

		# check signed in.
		if not self.authenticated:
			return dev0s.response.error("The current user is not authenticated.")

		# check already activated.
		if self.activated:
			return dev0s.response.error("The current user is already activated.")

		# check params.
		response = dev0s.response.parameters.check(
			parameters={
				"code:str":code,
			})
		if not response.success: return response

		# request.
		response = self.__request__("/requests/accounts/activate/", {
			"username":self.username,
			"code":code,
		})
		if response.success:
			self.__activated__ = True
		return response

		#

	# properties.
	@property
	def username(self):
		return self.__username__
	@property
	def email(self):
		return self.__email__
	@property
	def name(self):
		return self.__name__
	@property
	def api_key(self):
		return self.__api_key__
	@property
	def authenticated(self):
		return self.__authenticated__
	@property
	def activated(self):
		return self.__activated__
	@property
	def info(self):
		# public info.
		return {
			"username":self.username,
			"email":self.email,
			"name":self.name,
			"authenticated":self.authenticated,
			"activated":self.activated,
		}
	
	# system functions.
	def __request__(self, url="/", data={}, json=True, log_level=dev0s.defaults.options.log_level):
		url = f"api.vandenberghinc.com/{gfp.clean(url, remove_first_slash=True, remove_last_slash=True)}/"
		data["api_key"] = self.api_key
		return dev0s.requests.get(url=url, data=data, serialize=json)

# the initialized user object.
user = User()