from marshmallow import fields
from cc_py_commons.schemas.camel_case_schema import CamelCaseSchema

class LocationSchema(CamelCaseSchema):

  city = fields.String()
  state = fields.String()
  postcode = fields.String()
  county = fields.String() 
  country = fields.String()