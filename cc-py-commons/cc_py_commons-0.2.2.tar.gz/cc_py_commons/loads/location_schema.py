from marshmallow import fields
from cc_py_commons.schemas.camel_case_schema import CamelCaseSchema

class LocationSchema(CamelCaseSchema):

  city = fields.String()
  state = fields.String()
  postcode = fields.String(allow_none=True)
  county = fields.String(allow_none=True) 
  country = fields.String(allow_none=True)