import re
import decimal
from typing import Any, TYPE_CHECKING
from .exceptions import ValidationError

if TYPE_CHECKING:
	from .__init__ import InputItem, Schema


class Validator():
	'''
	A class to represent a base validator.

	...

	Attributes
	----------
	input_ : any
		the input that will be validated
	name : str
		the name of the input that will be validated

	Methods
	-------
	_set_parent_form(form):
		Set the parent schema

	required():
		Append a required validator in the input's validators list

	_required(value):
		Verify if the received value is empty
	'''

	def __init__(self, input_: 'InputItem') -> None:
		'''
		Constructs all the necessary attributes for the base validator object.

		Parameters
		----------
			input_ (InputItem): the input that will be validated
		'''

		self.input_ = input_
		self.name = input_.name

	def _set_parent_form(self, form: 'Schema') -> None:
		'''
		Set the parent schema of the validator's input

		Parameters
		----------
		form : Schema
			the validator's input parent schema

		Returns
		-------
		None
		'''

		self.input_.form = form

	def required(self) -> 'Validator':
		'''
		Append a required validator in the input's validators list

		Returns
		-------
		self (Validator): The validator itself
		'''

		self.input_ = self.input_.validate(self._required)
		return self

	def _required(self, value: Any) -> None:
		'''
		Verify if the received value is empty

		Parameters
		----------
		value : (Any)
			the value that will be checked

		Raises
		----------
		ValidationError:
			if the value is empty or None

		Returns
		________
		None
		'''

		if value is None or (not value and value != 0):
			raise ValidationError(self.name, 'Empty value passed to a required input')

	def verify(self):
		pass


class StringValidator(Validator):
	'''
	A class to represent a string validator, children of Validator.

	...

	Methods
	-------
	email():
		Append a email validator in the input's validators list

	_email(value):
		Verify if the received value is a valid email address

	min(min):
		Append a minimum validator in the input's validators list

	_min(min, value):
		Verify if the length of the received value is equal or higher than the min

	max(max):
		Append a maximum validator in the input's validators list

	_max(max, value):
		Verify if the length of the received value is equal or lower than the max

	verify():
		Get the validator's input value.
		If the value is not None converts it to a string and pass it to the input verify method
	'''

	def email(self) -> 'StringValidator':
		'''
		Append a email validator in the input's validators list

		Returns
		-------
		self (Validator): The validator itself
		'''

		self.input_ = self.input_.validate(self._email)
		return self

	def _email(self, value: str) -> None:
		'''
		Verify if the received value is a valid email address

		Parameters
		----------
		value : (str)
			the value that will be checked

		Raises
		----------
		ValidationError:
			if the value is not a valid email address

		Returns
		________
		None
		'''

		if re.fullmatch(r'[^@]+@[^@]+\.[^@]+', value) is None:
			raise ValidationError(self.name, 'Value for email type does not match a valid format')

	def min(self, value: int) -> 'StringValidator':
		'''
		Append a minimum validator in the input's validators list

		Parameters
		----------
		value : str
			the minimun length value that will be allowed

		Returns
		-------
		self (Validator): The validator itself
		'''

		self.input_ = self.input_.validate(lambda v: self._min(value, v))
		return self

	def _min(self, min: int, value: str) -> None:
		'''
		Verify if the length of the received value is equal or higher than the min

		Parameters
		----------
		value : (str)
			the value that will be checked
		min : (int)
			the minimun length allowed

		Raises
		----------
		ValidationError:
			if the value length is smaller than the min

		Returns
		________
		None
		'''

		if len(value) < min:
			raise ValidationError(self.name, 'Value too short received')

	def max(self, value: int) -> 'StringValidator':
		'''
		Append a maximum validator in the input's validators list

		Parameters
		----------
		value : str
			the maximun length value that will be allowed

		Returns
		-------
		self (Validator): The validator itself
		'''

		self.input_ = self.input_.validate(lambda v: self._max(value, v))
		return self

	def _max(self, max: int, value: str) -> None:
		'''
		Verify if the length of the received value is equal or lower than the max

		Parameters
		----------
		value : (str)
			the value that will be checked
		max : (int)
			the maximun length allowed

		Raises
		----------
		ValidationError:
			if the value length is larger than the max

		Returns
		________
		None
		'''

		if len(value) > max:
			raise ValidationError(self.name, 'Value too long received')

	def verify(self) -> dict:
		'''
		Get the validator's input value.
		If the value is not None converts it to a string and pass it to the input verify method

		Returns
		-------
		result (str): The value returned by the input verify method
		'''

		result = getattr(self.input_._input, self.input_._path)

		if callable(result):
			result = result()

		if result is not None:
			result = str(result)

		result = self.input_.verify(result)
		return result


class NumericValidator(Validator):
	'''
	A class to represent a Numeric validator, children of Validator.

	...

	Methods
	-------
	min(min):
		Append a minimum validator in the input's validators list

	_min(min, value):
		Verify if the received value is equal or higher than the min

	max(max):
		Append a maximum validator in the input's validators list

	_max(max, value):
		Verify if the received value is equal or lower than the max

	verify():
		Get the validator's input value.
		If the value is not None converts it to a string and pass it to the input verify method
	'''

	def min(self, value: int) -> 'NumericValidator':
		'''
		Append a minimum validator in the input's validators list

		Parameters
		----------
		value : int
			the minimun value that will be allowed

		Returns
		-------
		self (Validator): The validator itself
		'''

		self.input_ = self.input_.validate(lambda v: self._min(value, v))
		return self

	def _min(self, min: int, value: decimal.Decimal) -> None:
		'''
		Verify if the received value is equal or higher than the min

		Parameters
		----------
		value : (any)
			the value that will be checked
		min : (int)
			the minimun value allowed

		Raises
		----------
		ValidationError:
			if the value smaller than the min

		Returns
		________
		None
		'''

		if value < min:
			raise ValidationError(self.name, 'Value too small received')

	def max(self, value: int) -> 'NumericValidator':
		'''
		Append a maximum validator in the input's validators list

		Parameters
		----------
		value : str
			the maximun value that will be allowed

		Returns
		-------
		self (Validator): The validator itself
		'''

		self.input_ = self.input_.validate(lambda v: self._max(value, v))
		return self

	def _max(self, max: int, value: decimal.Decimal) -> None:
		'''
		Verify if the the received value is equal or lower than the max

		Parameters
		----------
		value : (any)
			the value that will be checked
		max : (int)
			the maximun length allowed

		Raises
		----------
		ValidationError:
			if the value is larger than the max

		Returns
		________
		None
		'''

		if value > max:
			raise ValidationError(self.name, 'Value too large received')

	def verify(self) -> dict:
		'''
		Get the validator's input value, converts it to a Decimal and pass it to the input verify method

		Raises
		----------
		ValidationError:
			if the conversion operation to Decimal is invalid

		Returns
		-------
		result (Decimal): The value returned by the input verify method
		'''

		result = getattr(self.input_._input, self.input_._path)

		if callable(result):
			result = result()

		try:
			value = decimal.Decimal(result)
		except decimal.InvalidOperation:
			raise ValidationError(self.name, 'Non-numeric value received in a numeric input')

		return self.input_.verify(value)
