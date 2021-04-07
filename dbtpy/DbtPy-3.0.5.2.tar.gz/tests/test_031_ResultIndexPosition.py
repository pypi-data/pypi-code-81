# 

#

#

import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_031_ResultIndexPosition(self):
     obj = DbtPyTestFunctions()
     obj.assert_expect(self.run_test_031)

  def run_test_031(self):
    conn = DbtPy.connect(config.ConnStr, config.user, config.password)
      
    if conn:
      stmt = DbtPy.exec_immediate(conn, "SELECT id, breed, name, weight FROM animals WHERE id = 0")
        
      while (DbtPy.fetch_row(stmt)):
        id = DbtPy.result(stmt, 0)
        print("int(%d)" % id)
        breed = DbtPy.result(stmt, 1)
        print("string(%d) \"%s\"" % (len(breed), breed))
        name = DbtPy.result(stmt, 2)
        print("string(%d) \"%s\"" % (len(name), name))
        weight = DbtPy.result(stmt, 3)
        print("string(%d) \"%s\"" % (len(str(weight)), weight))
      DbtPy.close(conn)
    else:
      print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#int(0)
#string(3) "cat"
#string(16) "Pook            "
#string(4) "3.20"
#__ZOS_EXPECTED__
#int(0)
#string(3) "cat"
#string(16) "Pook            "
#string(4) "3.20"
#__SYSTEMI_EXPECTED__
#int(0)
#string(3) "cat"
#string(16) "Pook            "
#string(4) "3.20"
#__IDS_EXPECTED__
#int(0)
#string(3) "cat"
#string(16) "Pook            "
#string(4) "3.20"
