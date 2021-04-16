from flask import Flask,session
from flask_restful import Api,Resource
from flask_cors import *
import datetime

from IutyApi.stock.monitor_ import MonitorApi
from IutyApi.stock.resistance_ import ResistanceApi
from IutyApi.task.todo_ import TodoApi
from IutyApi.usr.login_ import LoginApi
from IutyApi.dev.api_ import ApiApi

app = Flask(__name__,static_folder='static/',template_folder='static/template/')
api = Api(app)
CORS(app, supports_credentials=True)

host = '0.0.0.0'
port = 7780

app.config['SECRET_KEY'] = str(datetime.datetime.now())#'myskey'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME']=datetime.timedelta(days=30)

api.add_resource(MonitorApi,'/api/stock/monitor')
api.add_resource(ResistanceApi,'/api/stock/resistance')
api.add_resource(TodoApi,'/api/task/todo')
api.add_resource(LoginApi,'/api/usr/login')
api.add_resource(ApiApi,'/api/dev/api')

def main():
    app.run(host = host,port = port)

if __name__ == "__main__":
    main()
    pass
