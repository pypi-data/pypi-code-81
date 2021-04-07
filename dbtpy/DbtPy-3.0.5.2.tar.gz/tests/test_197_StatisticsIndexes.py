# 

#

#
# NOTE: IDS requires that you pass the schema name (cannot pass None)

import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_197_StatisticsIndexes(self):
    obj = DbtPyTestFunctions()
    obj.assert_expect(self.run_test_197)

  def run_test_197(self):
    conn = DbtPy.connect(config.ConnStr, config.user, config.password)
    server = DbtPy.server_info( conn )

    if conn:
      try:
          rc = DbtPy.exec_immediate(conn, "DROP TABLE index_test")
      except:
          pass
      rc = DbtPy.exec_immediate(conn, "CREATE TABLE index_test (id INTEGER, data VARCHAR(50))")
      rc = DbtPy.exec_immediate(conn, "CREATE UNIQUE INDEX index1 ON index_test (id)")

      print("Test first index table:")
      if (server.DBMS_NAME[0:3] == 'Inf'):
        result = DbtPy.statistics(conn,None,config.user,"index_test",True)
      else:
        result = DbtPy.statistics(conn,None,None,"INDEX_TEST",True)
      row = DbtPy.fetch_tuple(result)
      ## skipping table info row. statistics returns informtation about table itself for gbasedbt ###
      if (server.DBMS_NAME[0:3] == 'Inf'):
        row = DbtPy.fetch_tuple(result)
      print(row[2])  # TABLE_NAME
      print(row[3])  # NON_UNIQUE
      print(row[5])  # INDEX_NAME
      print(row[8])  # COLUMN_NAME

      try:
          rc = DbtPy.exec_immediate(conn, "DROP TABLE index_test2")
      except:
          pass
      rc = DbtPy.exec_immediate(conn, "CREATE TABLE index_test2 (id INTEGER, data VARCHAR(50))")
      rc = DbtPy.exec_immediate(conn, "CREATE INDEX index2 ON index_test2 (data)")

      print("Test second index table:")
      if (server.DBMS_NAME[0:3] == 'Inf'):
        result = DbtPy.statistics(conn,None,config.user,"index_test2",True)
      else:
        result = DbtPy.statistics(conn,None,None,"INDEX_TEST2",True)
      row = DbtPy.fetch_tuple(result)
      ### skipping table info row. statistics returns informtation about table itself for gbasedbt ###
      if (server.DBMS_NAME[0:3] == 'Inf'):
        row = DbtPy.fetch_tuple(result)
      print(row[2])  # TABLE_NAME
      print(row[3])  # NON_UNIQUE
      print(row[5])  # INDEX_NAME
      print(row[8])  # COLUMN_NAME

      print("Test non-existent table:")
      if (server.DBMS_NAME[0:3] == 'Inf'):
        result = DbtPy.statistics(conn,None,config.user,"non_existent_table",True)
      else:
        result = DbtPy.statistics(conn,None,None,"NON_EXISTENT_TABLE",True)
      row = DbtPy.fetch_tuple(result)
      if row:
        print("Non-Empty")
      else:
        print("Empty")
    else:
      print('no connection: ' + DbtPy.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#Test first index table:
#INDEX_TEST
#0
#INDEX1
#ID
#Test second index table:
#INDEX_TEST2
#1
#INDEX2
#DATA
#Test non-existent table:
#Empty
#__ZOS_EXPECTED__
#Test first index table:
#INDEX_TEST
#0
#INDEX1
#ID
#Test second index table:
#INDEX_TEST2
#1
#INDEX2
#DATA
#Test non-existent table:
#Empty
#__SYSTEMI_EXPECTED__
#Test first index table:
#INDEX_TEST
#0
#INDEX1
#ID
#Test second index table:
#INDEX_TEST2
#1
#INDEX2
#DATA
#Test non-existent table:
#Empty
#__IDS_EXPECTED__
#Test first index table:
#index_test
#0
#index1
#id
#Test second index table:
#index_test2
#1
#index2
#data
#Test non-existent table:
#Empty
