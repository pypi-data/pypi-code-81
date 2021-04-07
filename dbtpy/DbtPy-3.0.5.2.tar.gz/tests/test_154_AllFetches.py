# 

#

#

import unittest, sys
import DbtPy
import config
from testfunctions import DbtPyTestFunctions

class DbtPyTestCase(unittest.TestCase):

  def test_154_AllFetches(self):
    obj = DbtPyTestFunctions()
    obj.assert_expect(self.run_test_154)

  def run_test_154(self):
    conn = DbtPy.connect(config.ConnStr, config.user, config.password)

    server = DbtPy.server_info( conn )
    if (server.DBMS_NAME[0:3] == 'Inf'):
      op = {DbtPy.ATTR_CASE: DbtPy.CASE_UPPER}
      DbtPy.set_option(conn, op, 1)

    try:
        statement = 'DROP TABLE fetch_test'
        result = DbtPy.exec_immediate(conn, statement)
    except:
        pass
    
    server = DbtPy.server_info( conn )
    if (server.DBMS_NAME[0:3] == 'Inf'):
      statement = 'CREATE TABLE fetch_test (col1 VARCHAR(20), col2 CLOB, col3 INTEGER)'
      st0 = "INSERT INTO fetch_test VALUES ('column 0', FILETOCLOB('C:\\work\\DbtPy\\DbtPy\\tests\\data\\data1.txt','client'), 0)"
      st1 = "INSERT INTO fetch_test VALUES ('column 1', FILETOCLOB('C:\\work\\DbtPy\\DbtPy\\tests\\data\\data2.txt','client'), 1)"
      st2 = "INSERT INTO fetch_test VALUES ('column 2', FILETOCLOB('C:\\work\\DbtPy\\DbtPy\\tests\\data\\data3.txt','client'), 2)"
      st3 = "INSERT INTO fetch_test VALUES ('column 3', FILETOCLOB('C:\\work\\DbtPy\\DbtPy\\tests\\data\\data4.txt','client'), 3)"
    else:
      statement = 'CREATE TABLE fetch_test (col1 VARCHAR(20), col2 CLOB(20), col3 INTEGER)'
      st0 = "INSERT INTO fetch_test VALUES ('column 0', FILETOCLOB('C:\\work\\DbtPy\\DbtPy\\tests\\data\\data1.txt','client'), 0)"
      st1 = "INSERT INTO fetch_test VALUES ('column 1', FILETOCLOB('C:\\work\\DbtPy\\DbtPy\\tests\\data\\data2.txt','client'), 1)"
      st2 = "INSERT INTO fetch_test VALUES ('column 2', FILETOCLOB('C:\\work\\DbtPy\\DbtPy\\tests\\data\\data3.txt','client'), 2)"
      st3 = "INSERT INTO fetch_test VALUES ('column 3', FILETOCLOB('C:\\work\\DbtPy\\DbtPy\\tests\\data\\data4.txt','client'), 3)"
    result = DbtPy.exec_immediate(conn, statement)

    result = DbtPy.exec_immediate(conn, st0)
    result = DbtPy.exec_immediate(conn, st1)
    result = DbtPy.exec_immediate(conn, st2)
    result = DbtPy.exec_immediate(conn, st3)

    statement = "SELECT col1, col2 FROM fetch_test"
    result = DbtPy.prepare(conn, statement)
    DbtPy.execute(result)

    row = DbtPy.fetch_tuple(result)
    while ( row ):
      #printf("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long.\n",
      #        row[0],row[0].length, row[1],row[1].length)
      print("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long." %\
        (row[0], len(row[0]), row[1], len(row[1])))
      row = DbtPy.fetch_tuple(result)

    result = DbtPy.prepare(conn, statement)
    DbtPy.execute(result)

    row = DbtPy.fetch_assoc(result)
    while ( row ):
      #printf("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long.\n",
      #        row['COL1'], row['COL1'].length, row['COL2'], row['COL2'].length)
      print("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long." %\
        (row['COL1'], len(row['COL1']), row['COL2'], len(row['COL2'])))
      row = DbtPy.fetch_assoc(result)
      
    result = DbtPy.prepare(conn, statement)
    DbtPy.execute(result)

    row = DbtPy.fetch_both(result)
    while ( row ):
      #printf("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long.\n",
      #        row['COL1'], row['COL1'].length, row[1], row[1].length)
      print("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long.\n" % \
        (row['COL1'],len(row['COL1']), row[1], len(row[1])))
      row = DbtPy.fetch_both(result)

    DbtPy.close(conn)

#__END__
#__LUW_EXPECTED__
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#__ZOS_EXPECTED__
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#__SYSTEMI_EXPECTED__
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#__IDS_EXPECTED__
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
#"column 0" from VARCHAR is 8 bytes long, "Data in the clob 0" from CLOB is 18 bytes long.
#"column 1" from VARCHAR is 8 bytes long, "Data in the clob 1" from CLOB is 18 bytes long.
#"column 2" from VARCHAR is 8 bytes long, "Data in the clob 2" from CLOB is 18 bytes long.
#"column 3" from VARCHAR is 8 bytes long, "Data in the clob 3" from CLOB is 18 bytes long.
