import os

db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")

APP_VERSION = os.environ.get("APP_VERSION")

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
