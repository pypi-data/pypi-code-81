'''
SMWinservice
by Davide Mastromatteo
Base class to create winservice in Python
-----------------------------------------
Instructions:
1. Just create a new class that inherits from this base class
2. Define into the new class the variables
   _svc_name_ = "nameOfWinservice"
   _svc_display_name_ = "name of the Winservice that will be displayed in scm"
   _svc_description_ = "description of the Winservice that will be displayed in scm"
3. Override the three main methods:
    def start(self) : if you need to do something at the service initialization.
                      A good idea is to put here the inizialization of the running condition
    def stop(self)  : if you need to do something just before the service is stopped.
                      A good idea is to put here the invalidation of the running condition
    def main(self)  : your actual run loop. Just create a loop based on your running condition
4. Define the entry point of your module calling the method "parse_command_line" of the new class
5. Enjoy
'''

import datetime
import logging
import os
import socket
import sys
import time
import servicemanager
import win32event
import win32service
import win32serviceutil
from .logger import createRotatingLogger, createSlackLogger
import pyodbc


class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'SMWinserviceTest'
    _svc_display_name_ = 'SMWinserviceTest'
    _svc_description_ = 'Python Service Description'
    _svc_logger_ = 'pythonService_logger'
    _looptime_ = 5
    _daily_ = None
    _svc_logpath_ = 'C:\\logs\\pythonService\\'
    args = []
    logger = None
    slacker = None
    finish_query = """
        UPDATE EasyPostServices.dbo.Services 
        SET LastRunDateTime = GETDATE(),
            LastFinishStatus = '{status}'
        WHERE ServiceName = '{table}';
        IF NOT EXISTS(SELECT 1 FROM (SELECT TOP(1) * FROM EasyPostServices.dbo.{table} ORDER BY DateTime DESC) one WHERE  Type = '{status_type}' AND Description = '{status_description}')
        BEGIN
            INSERT INTO EasyPostServices.dbo.{table}
                (DateTime
                ,Type
                ,Description)
            VALUES
                (GETDATE()
                ,'{status_type}'
                ,'{status_description}')
        END
        ELSE
        BEGIN
            UPDATE EasyPostServices.dbo.{table}
            SET DateTime = GETDATE(),
                SequentialOccurrences = SequentialOccurrences + 1
            WHERE Id in (SELECT TOP(1) Id FROM EasyPostServices.dbo.{table} ORDER BY DateTime DESC)
        END
    """
    start_query = """
        IF EXISTS 
        (
            SELECT 1
            FROM EasyPostServices.dbo.Services 
            WHERE ServiceName = '{table}'
        )
            BEGIN
                UPDATE EasyPostServices.dbo.Services 
                SET LastStartDateTime = GETDATE(),
                    ServiceDescription = '{description}',
                    StatusLogs = 'EasyPostServices.dbo.{table}',
                    LoopTime = {looptime},
                    DailyHour = {daily}
                WHERE ServiceName = '{table}'
            END
        ELSE
            BEGIN
                INSERT INTO EasyPostServices.dbo.Services 
                (ServiceName
                ,ServiceDescription
                ,StatusLogs
                ,LastStartDateTime
                ,LastRunDateTime
                ,LastFinishStatus
                ,LoopTime
                ,DailyHour)
                VALUES
                    (
                    '{table}'
                    ,'{description}'
                    ,'EasyPostServices.dbo.{table}'
                    ,GETDATE()
                    ,'1997-01-01 00:00'
                    ,'1997-01-01 00:00'
                    ,{looptime}
                    ,{daily}
                    )
            END
    """
    query = """
                    IF NOT EXISTS(SELECT 1 FROM sys.Tables WHERE  Name = N'{table}' AND Type = N'U')
                    BEGIN
                        CREATE TABLE  EasyPostServices.dbo.{table}(
                            Id int IDENTITY(1,1) NOT NULL,
                            DateTime datetime NOT NULL,
                            Type varchar(10) NOT NULL,
                            Description varchar(max) NOT NULL,
                            SequentialOccurrences int NOT NULL,
                            CONSTRAINT PK_{table} PRIMARY KEY CLUSTERED 
                        (
                            Id ASC
                        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
                        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
                        
                        ALTER TABLE  EasyPostServices.dbo.{table} ADD  CONSTRAINT DF_{table}_Description  DEFAULT ('') FOR Description
                        ALTER TABLE EasyPostServices.dbo.{table} ADD  CONSTRAINT DF_{table}_SequentialOccurrences  DEFAULT ((1)) FOR SequentialOccurrences
                        SET ANSI_NULLS ON
                        SET QUOTED_IDENTIFIER ON
                    END
        """
    
    def connect_to_db(self,retry=0):
        try:
            db_conn = pyodbc.connect(driver = '{SQL Server Native Client 11.0}',
                                        server = '10.10.10.30,1433',
                                        database = 'EasyPostServices',                                       
                                        user = 'sa',
                                        password = 'sql')
            
            return db_conn
        except pyodbc.Error as e:      
            if retry < 4:
                return self.connect_to_db(retry=retry+1)
            else:
                print("SQL connection error, ocr", e)
                return False
    
    def setup_db(self,retry=0):
        db_conn = self.connect_to_db()
        if db_conn:
            try:
                cursor = db_conn.cursor()
                cursor.execute(self.query.format(table = self._svc_name_))
                cursor.commit()
                cursor.close()
                db_conn.close()
                return True
            except Exception as ex:
                if retry < 4:
                    return self.setup_db(retry=retry+1)
                else:
                    if self.slacker:
                        self.slacker.log("Starting Service DataBase Write Failed\n" + str(ex))
                    if self.logger:
                        self.logger.error("Starting Service DataBase Write Failed : " + str(ex))
        return False

    def write_to_db(self,status = 'start', options=['FINISH','SUCCESS'],retry=0):
        db_conn = self.connect_to_db()
        print("got db conn")
        print(db_conn)
        if db_conn:
            try:
                cursor = db_conn.cursor()
                print("got cursor")
                if self._daily_:
                    temp_daily = str(self._daily_)
                else:
                    temp_daily = 'NULL'
                print(temp_daily)
                if status == 'start':
                    cursor.execute(self.start_query.format(table=self._svc_name_,description=self._svc_description_,looptime=str(self._looptime_),daily=temp_daily))
                    print(self.start_query.format(table=self._svc_name_,description=self._svc_description_,looptime=str(self._looptime_),daily=temp_daily))
                if status == 'finish':
                    cursor.execute(self.finish_query.format(table=self._svc_name_,status=options[0],status_type='FINISH',status_description=options[1]))
                if status == 'error':
                    cursor.execute(self.finish_query.format(table=self._svc_name_,status=options[0],status_type='ERROR',status_description=options[1]))
                print("executed: " + str(status))
                cursor.commit()
                cursor.close()
                db_conn.close()
                print("closed all")
                return True
            except Exception as ex:
                if retry < 4:
                    return self.write_to_db(status = status, options= options,retry=retry+1)
                else:
                    if self.slacker:
                        self.slacker.log("Starting Service DataBase Write Failed\n" + str(ex))
                    if self.logger:
                        self.logger.error("Starting Service DataBase Write Failed : " + str(ex))
        return False

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)
    
    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        self._svc_display_name_ = self.__class__.__name__
        print(self._svc_display_name_)
        self._svc_name_= self.__class__.__name__
        print(self._svc_name_)
        self.args = [arg for arg in args]
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.isrunning = False
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self._svc_logger_ = self._svc_name_ + '_logger'
        self._svc_logpath_ = 'C:\\logs\\' + self._svc_name_ + '\\'
        if not os.path.exists(self._svc_logpath_):
            os.makedirs(self._svc_logpath_)
        self.logger = createRotatingLogger(self._svc_logger_ , self._svc_logpath_)
        self.slacker = createSlackLogger(self._svc_name_,self.logger)
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.isrunning = True
        print("seting up db")
        if self.setup_db():
            print("success setup")
        else:
            print("failed setup")

        self.main()
        print("passed main")


    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        self.write_to_db(status='start')
        print("written to db")
        if self._daily_:
            checker = datetime.datetime.now()
            # checks if next loop should start or not every second
            while self.isrunning:
                if datetime.datetime.now() > checker:
                    checker += datetime.timedelta(seconds=self._looptime_)
                    # wait for 14h
                    if datetime.datetime.now().hour == self._daily_:
                        checker += datetime.timedelta(hours=24,seconds=-self._looptime_)
                        try:
                            self.logger.debug("loop service: " + self._svc_name_)
                            result = str(self.loop())
                            self.write_to_db(status='finish',options=[result,result])
                        except Exception as e:
                            self.logger.error("Exception executing run: " + str(e))
                            self.write_to_db(status='error',options=['FAIL',str(e)])
            time.sleep(1)
        else:
            checker = datetime.datetime.now()
            # checks if next loop should start or not every second
            while self.isrunning:
                if datetime.datetime.now() > checker:
                    try:
                        self.logger.debug("-----------started loop--" + str(checker) + "-----------")
                        result = str(self.loop())
                        self.write_to_db(status='finish',options=[result,result])
                        self.logger.debug("-----------ended loop--" + str(checker) + "-----------")
                    except Exception as e:
                        self.logger.error("Exception executing run: " + str(e))
                        self.write_to_db(status='error',options=['FAIL',str(e)])
                    checker += datetime.timedelta(seconds=self._looptime_)
                time.sleep(1)
            
    def loop(self):
        return self.run()

    def run(self):
        '''
        Run to be overridden to add script
        '''
        raise NotImplementedError

# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    SMWinservice.parse_command_line()