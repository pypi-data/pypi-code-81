from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import DeleteRowsEvent,UpdateRowsEvent,WriteRowsEvent
import clickhouse_driver

class BinLogLoader(object):

    '''
    use mysql binlog to add data (insert,update,delete) to clickhouse
    '''

    def __init__(self,mysql_settings,clickhouse_settings,table_mapping,server_id=1,blocking=False,log_file=None,log_pos=None):
        '''
        mysql_settings: mysql configs to pass in BinLogStreamReader. 
        example: {'host': '192.168.3.9','port': 3306,'user': 'thomas', 'passwd': '901018'}

        clickhouse_settings: clickhouse configs to create clickhouse_driver client
        example: {'host':'192.168.3.9','port':9100,'user':'default','password':'','database':'zftest'}

        table_mapping:schema and tablename mapping from mysql to clickhouse
        example: {('zftest','HistPrice'):('zftest','HistPrice_all')}

        server_id: server_id passed to BinLogStreamReader.

        blocking: BinLogStreamReader param, When master has finished reading/sending binlog it will send EOF instead of blocking connection.

        log_file: log filename to start 

        log_pos: log pos to start 

        '''
        self.table_mapping = table_mapping
        kwargs = {}
        kwargs['connection_settings'] = mysql_settings
        kwargs['resume_stream'] = True
        kwargs['server_id'] = server_id
        kwargs['blocking'] = blocking
        pairs = table_mapping.keys()
        kwargs['only_schemas'] = [a for (a,b) in pairs] 
        kwargs['only_tables'] = [b for (a,b) in pairs] 
        if log_file is not None and log_pos is not None:
            kwargs['log_file'] = log_file
            kwargs['log_pos'] = log_pos
        kwargs['only_events'] = [DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent]
        self.kwargs = kwargs
        self.client = clickhouse_driver.Client(**clickhouse_settings)

    def load(self,keep_listening=False,record_filepath=None,ignore_errors=False):
        '''
        load data using binlog.
        there are 2 modes, identified by keep_listening:
        (1) false, exit when finishing all binlogs.
        (2) true, dont exit and wait for new event 
            need to provide a file to record log name and log pos.

        ignore_errors: whether ignore errors during the process.
        if true, load function will ignore the errors, and keep loading the rest.

        clickhouse table must have a Status column:
        1: insert, 2: update, 3: delete

        '''
        if keep_listening:
            if record_filepath is None:
                raise Exception('record_filepath parameter is missing,you need provide a record_filepath under keep_listening mode')
            self.kwargs['blocking'] = True

        stream = BinLogStreamReader(**self.kwargs)
        for binlogevent in stream:
            for row in binlogevent.rows:
                try:
                    schema_from = binlogevent.schema
                    table_from = binlogevent.table
                    schema_to, table_to = self.table_mapping[(schema_from,table_from)] 
                    if isinstance(binlogevent, WriteRowsEvent):
                        data = row["values"]
                        data['Status'] = 1
                    elif isinstance(binlogevent, UpdateRowsEvent):
                        data = row["after_values"]
                        data['Status'] = 2
                    elif isinstance(binlogevent, DeleteRowsEvent):
                        data = row["values"]
                        data['Status'] = 3

                    sql_str = self._gen_query(data,schema_to,table_to)
                    self.client.execute(sql_str)
                except Exception as e:
                    print(str(e))
                    if not ignore_errors:
                        stream.close()
                        raise Exception('error at logfile:{},pos:{}...'.format(stream.log_file,stream.log_pos) + str(e))
            self.kwargs['log_file'] = stream.log_file
            self.kwargs['log_pos'] = stream.log_pos
            if record_filepath: 
                with open(record_filepath,'w') as f:
                    f.write('{},{}'.format(self.kwargs['log_file'],self.kwargs['log_pos']))
        if not keep_listening:
            stream.close()
            return self.kwargs['log_file'], self.kwargs['log_pos']
    def _gen_query(self,data,schema,table):
        for k,v in data.items():
            if v is None:
                data[k] = "NULL"
            else:
                data[k] = "'{}'".format(str(v))
        sql_str = "insert into {}.{} ({}) values ({})".format(schema,table,",".join(data.keys()),",".join(data.values()))
        return sql_str

if __name__ == '__main__':
    mysql_settings = {'host': '192.168.3.9','port': 3306,'user': 'thomas', 'passwd': '123456'}
    clickhouse_settings = {'host':'192.168.3.9','port':9100,'user':'default','password':'','database':'zftest'}
    table_mapping = {('zftest','HistPrice'):('zftest','HistPrice_all')}
    bl = BinLogLoader(mysql_settings,clickhouse_settings,table_mapping,log_file='binlog.000009',log_pos=2345)
    bl.load(record_filepath = './record_file')

