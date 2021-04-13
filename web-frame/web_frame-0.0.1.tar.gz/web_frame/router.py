# 路由配置
from web_frame.frame.DocHandler import DocHandler, RecordHandler

router = [(r"/doc", DocHandler), (r'/record', RecordHandler)]
