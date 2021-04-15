import os

SCHOOL_NAME = os.environ.get("SCHOOL_NAME", "北京好专业考勤管理学校")
NICE_SECRET_KEY = os.environ.get("NICE_SECRET_KEY", "ff48dec875cc56f330b28f14388b05e9")
NICE_APP_KEY = os.environ.get("NICE_APP_KEY", "21b190d5785837695e8cade16410be3a")
NICE_PROTOCOL = os.environ.get("NICE_PROTOCOL", "https")
NICE_HOST = os.environ.get("NICE_HOST", "xgk.lanzhou.edu.cn/schoolscheduleserv/integration")
# NICE_HOST = os.environ.get("NICE_HOST", "connect.nicezhuanye.com/schoolscheduleserv/integration")

NIRVANA_PROTOCOL = os.environ.get("NIRVANA_PROTOCOL", "http")
NIRVANA_HOST = os.environ.get("NIRVANA_HOST", "10.100.1.23")
NIRVANA_PORT = int(os.environ.get("NIRVANA_PORT", 14001))
NIRVANA_TOKEN = os.environ.get("NIRVANA_TOKEN", "skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=")

EDTECH_SERVER_URL = os.environ.get("EDTECH_SERVER_URL", "http://10.100.1.23:12363")
EDTECH_SERVER_TOKEN = os.environ.get("EDTECH_SERVER_TOKEN", "Token 6c5a192e3e161342489971b10d36dee5250e64dd")
CLASS_CARD_SERVER_URL = os.environ.get("CLASS_CARD_SERVER_URL", "http://10.100.1.23:14001")
CLASS_CARD_SERVER_TOKEN = os.environ.get("CLASS_CARD_SERVER_TOKEN", "Skeleton gjtxsjtyjsxqsl Z2p0eHNqdHlqc3hxc2w=")

