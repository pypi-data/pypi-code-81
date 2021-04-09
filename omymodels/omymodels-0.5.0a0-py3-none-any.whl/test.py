from omymodels import create_models

ddl = """
CREATE TABLE "prefix--schema-name"."table" (
  _id uuid PRIMARY KEY,
);
"""
result = create_models(ddl)
print(result)
