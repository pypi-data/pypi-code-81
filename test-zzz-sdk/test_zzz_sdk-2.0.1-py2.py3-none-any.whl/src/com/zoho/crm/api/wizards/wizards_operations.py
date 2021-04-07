try:
	from zcrmsdk.src.com.zoho.crm.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.crm.api.param import Param
except Exception:
	from ..exception import SDKException
	from ..util import APIResponse, CommonAPIHandler, Constants
	from ..param import Param


class WizardsOperations(object):
	def __init__(self, layout_id=None):
		"""
		Creates an instance of WizardsOperations with the given parameters

		Parameters:
			layout_id (string) : A string representing the layout_id
		"""

		if layout_id is not None and not isinstance(layout_id, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: layout_id EXPECTED TYPE: str', None, None)
		
		self.__layout_id = layout_id


	def get_wizards(self):
		"""
		The method to get wizards

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2.1/settings/wizards'
		handler_instance.set_api_path(api_path)
		handler_instance.set_http_method(Constants.REQUEST_METHOD_GET)
		handler_instance.set_category_method(Constants.REQUEST_CATEGORY_READ)
		handler_instance.add_param(Param('layout_id', 'com.zoho.crm.api.Wizards.GetWizardsParam'), self.__layout_id)
		try:
			from zcrmsdk.src.com.zoho.crm.api.wizards.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def get_wizard_by_id(self, wizard_id):
		"""
		The method to get wizard by id

		Parameters:
			wizard_id (int) : An int representing the wizard_id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if not isinstance(wizard_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: wizard_id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2.1/settings/wizards/'
		api_path = api_path + str(wizard_id)
		handler_instance.set_api_path(api_path)
		handler_instance.set_http_method(Constants.REQUEST_METHOD_GET)
		handler_instance.set_category_method(Constants.REQUEST_CATEGORY_READ)
		handler_instance.add_param(Param('layout_id', 'com.zoho.crm.api.Wizards.GetWizardbyIDParam'), self.__layout_id)
		try:
			from zcrmsdk.src.com.zoho.crm.api.wizards.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')


class GetWizardsParam(object):
	pass


class GetWizardbyIDParam(object):
	pass
