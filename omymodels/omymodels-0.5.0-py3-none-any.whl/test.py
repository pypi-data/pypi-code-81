from omymodels import create_models

ddl = """
CREATE TABLE "prefix--schema-name"."table" (
  _id uuid PRIMARY KEY,
  one_more_id int
);
    create unique index table_pk on "prefix--schema-name"."table" (one_more_id) ;
    create index table_ix2 on "prefix--schema-name"."table" (_id) ;
"""
result = create_models(ddl, schema_global=False)
print(result)
