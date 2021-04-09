from marshmallow import fields
from cc_py_commons.schemas.camel_case_schema import CamelCaseSchema

class ContactSchema(CamelCaseSchema):
  first_name: fields.String()
  last_name: fields.String()
  phone: fields.String()
  email_address: fields.Email()