from omymodels import create_models

ddl = """
CREATE TYPE "schema--notification"."ContentType" AS
 ENUM ('TEXT','MARKDOWN','HTML');
CREATE TABLE "schema--notification"."notification" (
    content_type "schema--notification"."ContentType"
);
"""
result = create_models(ddl)
print(result)
