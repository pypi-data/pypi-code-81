# 

#

#

import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_116_ConnActive(self):
    obj = DbtPyTestFunctions()
    obj.assert_expect(self.run_test_116)

  def run_test_116(self):
    conn = None
    is_alive = DbtPy.active(conn)
    if is_alive:
      print("Is active")
    else:
      print("Is not active")

    conn = DbtPy.connect(config.ConnStr, config.user, config.password)
    is_alive = DbtPy.active(conn)
    if is_alive:
      print("Is active")
    else:
      print("Is not active")

    DbtPy.close(conn)
    is_alive = DbtPy.active(conn)
    if is_alive:
      print("Is active")
    else:
      print("Is not active")

    # Executing active method multiple times to reproduce a customer reported defect
    print(DbtPy.active(conn))
    print(DbtPy.active(conn))
    print(DbtPy.active(conn))
    conn = DbtPy.connect(config.ConnStr, config.user, config.password)
    print(DbtPy.active(conn))
    print(DbtPy.active(conn))
    print(DbtPy.active(conn))

#__END__
#__LUW_EXPECTED__
#Is not active
#Is active
#Is not active
#False
#False
#False
#True
#True
#True
#__ZOS_EXPECTED__
#Is not active
#Is active
#Is not active
#False
#False
#False
#True
#True
#True
#__SYSTEMI_EXPECTED__
#Is not active
#Is active
#Is not active
#False
#False
#False
#True
#True
#True
#__IDS_EXPECTED__
#Is not active
#Is active
#Is not active
#False
#False
#False
#True
#True
#True
