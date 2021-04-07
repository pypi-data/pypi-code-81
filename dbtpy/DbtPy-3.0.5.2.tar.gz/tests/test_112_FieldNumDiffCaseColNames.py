# 

#

#

import unittest, sys
import DbtPy
import config
import os
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_112_FieldNumDiffCaseColNames(self):
    obj = DbtPyTestFunctions()
    obj.assert_expect(self.run_test_112)

  def run_test_112(self):
    os.environ['DELIMIDENT'] = 'y'
    conn = DbtPy.connect(config.ConnStr, config.user, config.password)

    if conn:
      drop = "DROP TABLE ftest"
      try:
        DbtPy.exec_immediate( conn, drop )
      except:
        pass
      
      create = "CREATE TABLE ftest ( \"TEST\" INTEGER, \"test\" INTEGER, \"Test\" INTEGER  )"
      DbtPy.exec_immediate(conn, create)
      
      insert = "INSERT INTO ftest VALUES (1,2,3)"
      DbtPy.exec_immediate(conn, insert)
      
      stmt = DbtPy.exec_immediate(conn, "SELECT * FROM ftest")
    
      num1 = DbtPy.field_num(stmt, "TEST")
      num2 = DbtPy.field_num(stmt, 'test')
      num3 = DbtPy.field_num(stmt, 'Test')
      
      print("int(%d)" % num1)
      print("int(%d)" % num2)
      print("int(%d)" % num3)
      
    else:
      print("Connection failed.")

#__END__
#__IDS_EXPECTED__
#int(0)
#int(1)
#int(2)
