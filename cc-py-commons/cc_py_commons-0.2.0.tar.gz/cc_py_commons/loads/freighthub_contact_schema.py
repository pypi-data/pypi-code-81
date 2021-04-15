from marshmallow import fields
from cc_py_commons.schemas.camel_case_schema import CamelCaseSchema

class FreightHubContactSchema(CamelCaseSchema):
  contact_name = fields.String()
  contact_phone = fields.String()
  contact_fax = fields.String()
  contact_email = fields.String()
  company_name = fields.String()
  user_id = fields.String()