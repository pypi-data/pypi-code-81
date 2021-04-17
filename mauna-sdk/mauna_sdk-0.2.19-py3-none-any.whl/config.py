import os


API_ENDPOINT = os.environ.get("MAUNA_API_ENDPOINT", "https://api.mauna.cloud/v1/graphql")
AUTH_ENDPOINT = os.environ.get("MAUNA_AUTH_ENDPOINT", "https://sdk.mauna.cloud/generateHasuraJWT")
