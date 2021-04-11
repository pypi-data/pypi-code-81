import enum

API_ROOT = "/api/v1"


class Endpoints(str, enum.Enum):
    """Enum of API endpoints."""

    # Auth
    ACCESS_TOKEN = API_ROOT + "/login/access-token"
    TEST_TOKEN = API_ROOT + "/login/test-token"

    # Users
    USERS = API_ROOT + "/users/"
    ME = API_ROOT + "/users/me"

    # Objects - ensure the object endpoints end in slash
    ASSETS = API_ROOT + "/assets/"
    PERIODICITIES = API_ROOT + "/periodicities/"
    CANDLES = API_ROOT + "/candles/"
    PATTERNS = API_ROOT + "/patterns/"
    INDICATORS = API_ROOT + "/indicators/"
