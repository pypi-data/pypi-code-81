# 

#

#

import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_030_Result(self):
    obj = DbtPyTestFunctions()
    obj.assert_expect(self.run_test_030)

  def run_test_030(self):
    conn = DbtPy.connect(config.ConnStr, config.user, config.password)
    server = DbtPy.server_info( conn )

    if conn:
      stmt = DbtPy.exec_immediate(conn, "SELECT id, breed, name, weight FROM animals WHERE id = 0")

      while (DbtPy.fetch_row(stmt)):
        breed = DbtPy.result(stmt, 1)
        print("string(%d) \"%s\"" % (len(breed), breed))
        name = DbtPy.result(stmt, "name")
        print("string(%d) \"%s\"" % (len(name), name))
      DbtPy.close(conn)
        
    else:
      print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#string(3) "cat"
#string(16) "Pook            "
#__ZOS_EXPECTED__
#string(3) "cat"
#string(16) "Pook            "
#__SYSTEMI_EXPECTED__
#string(3) "cat"
#string(16) "Pook            "
#__IDS_EXPECTED__
#string(3) "cat"
#string(16) "Pook            "
