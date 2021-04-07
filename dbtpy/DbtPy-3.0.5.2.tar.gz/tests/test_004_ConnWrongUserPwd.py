# 

#

#

import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_004_ConnWrongUserPwd(self):
    obj = DbtPyTestFunctions()
    obj.assert_expect(self.run_test_004)

  def run_test_004(self):
    try:
      conn = DbtPy.connect("sample", "not_a_user", "inv_pass")
    except:
      print("connect failed, test succeeded")
      return -1
    print("connect succeeded? Test failed")

#__END__
#__LUW_EXPECTED__
#connect failed, test succeeded
#__ZOS_EXPECTED__
#connect failed, test succeeded
#__SYSTEMI_EXPECTED__
#connect failed, test succeeded
#__IDS_EXPECTED__
#connect failed, test succeeded
