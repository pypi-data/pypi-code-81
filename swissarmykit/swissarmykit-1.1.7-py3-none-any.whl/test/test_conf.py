import os
import time

os.environ['SWISSARMYKIT_DEBUG'] = '1'

from swissarmykit.conf import *
from swissarmykit.conf import *
from swissarmykit.conf import *

# print(swissarmykit_conf)


# print(appConfig.start_ts())
# time.sleep(2)
# print(appConfig.get_ts_duration())
#
# print(appConfig.start_ts())
# time.sleep(3)
# print(appConfig.get_ts_duration())
#
# print(appConfig.timeit_ts)


print('\ncheckpoint 2: ', appConfig.start_ts(2))
time.sleep(4)
print(appConfig.get_ts_duration(2))
print(appConfig.timeit_ts)
