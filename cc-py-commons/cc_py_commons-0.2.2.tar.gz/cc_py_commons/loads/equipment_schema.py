from marshmallow import fields
from cc_py_commons.schemas.camel_case_schema import CamelCaseSchema

class EquipmentSchema(CamelCaseSchema):
  
  id = fields.UUID()
  name = fields.String()