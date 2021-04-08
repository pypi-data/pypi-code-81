# -*- coding: utf-8 -*-
import os
DB_URL = {'sly': 'mysql+mysqlconnector://quant:quant@192.168.199.137/quant' if 'SYL_DB' not in os.environ else os.environ['SYL_DB']}

server = ('api.p1.seleyatech.com', 50008, 'api.jdw.smartdata-x.top', 443)