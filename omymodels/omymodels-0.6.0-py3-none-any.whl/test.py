from omymodels import create_models

ddl = """
  
  CREATE TABLE order_items (
      product_no integer REFERENCES products ON DELETE RESTRICT,
      order_id integer REFERENCES orders ON DELETE CASCADE,
      type integer REFERENCES types (type_id) ON UPDATE CASCADE ON DELETE RESTRICT,
      PRIMARY KEY (product_no, order_id)
  );
  
"""
result = create_models(ddl, schema_global=False)
print(result)
import pprint
pprint.pprint(result['metadata'])
