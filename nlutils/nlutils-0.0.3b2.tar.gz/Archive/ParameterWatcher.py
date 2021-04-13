import json
import os
import time
import pymongo

from multiprocessing import Process, Queue
from hashlib import md5
from functools import singledispatch
from datetime import datetime
from functools import partial

from ..Utils.Log import Logger
from ..CommonDefine import ParameterType, DEV_MODE, DevelopMode, ParameterHandlerOperation




PARAMETER_OPERATION_DISPATCHER_THEME = {
    ParameterType.MODEL: None,
    ParameterType.DATA: None,
    ParameterType.TRANINING: None,
    ParameterType.MISCELLANEOUS: None,
    'Initialized': False
}

VALID_OPERATION_TYPE = ('INSERT', 'DELETE', 'UPDATE', 'SELECT')
NECESSARY_KEYS = {'parameter_type', 'operation_type'}

PARAMETER_OPERATION_DISPATCHER_OP = {
    ParameterHandlerOperation.INSERT: None,
    ParameterHandlerOperation.DELETE: None,
    ParameterHandlerOperation.UPDATE: None,
    ParameterHandlerOperation.SELECT: None,
    'Initialized': False
}

def get_md5_hash(obj):
    md5_obj = md5()
    md5_obj.update(obj.encode('utf8'))
    return md5_obj.hexdigest()

def handle_args_parser_params(args):
    # print(args._get_kwargs())
    arg_parse_dict = {'parameter_type': ParameterType.MISCELLANEOUS, 'operation_type': ParameterHandlerOperation.INSERT}
    arg_parse_dict['insert_keys'] = []
    for kwarg in args._get_kwargs():
        arg_parse_dict[kwarg[0]] = arg_parse_dict[kwarg[1]]
        arg_parse_dict['insert_keys'].append(kwarg[0])
    return arg_parse_dict

class ParameterWatcher(object):

    @classmethod
    def config_mongodb_server(cls, host:str, ip:int, username:str, password:str):
        cls.mongodb = dict()
        cls.mongodb['host'] = host
        cls.mongodb['port'] = port
        cls.mongodb['username'] = username
        cls.mongodb['password'] = password

        cls.myclient = pymongo.MongoClient(host=cls.mongodb['host'], port=cls.mongodb['host'], connect=False)
        # cls.myclient = pymongo.MongoClient("mongodb://47.103.90.218:8752/", connect=False)
        cls.db = cls.myclient.admin
        cls.db.authenticate(cls.mongodb['username'], cls.mongodb['password'])
        
        cls._configed = True
        


    @classmethod
    def save_to_file(cls, save_path='./params', save_to_cloud=False):
        if save_to_cloud and not cls._configed:
            raise ValueError(f"save_to_cloud cannot be set to {save_to_cloud} becasuse cls._configured is False")
        while True:
            # if cls.WATCHER_QUEUE.empty():
            #     Logger.get_logger().warning("Empty queue, skipping this round...")
            #     time.sleep(2)
            #     continue
            watcher = cls.WATCHER_QUEUE.get()
            whole_data = dict()
            whole_data['name'] = watcher.name
            whole_data['description'] = watcher.description
            whole_data['model_parameters'] = watcher.model_parameters
            whole_data['training_parameters'] = watcher.training_parameters
            whole_data['data_parameters'] = watcher.data_parameters
            whole_data['miscellaneous_parameters'] = watcher.data_parameters
            whole_data['models'] = watcher.models
            whole_data['results'] = watcher.results
            hash_code = get_md5_hash(whole_data.__str__())
            whole_data['time'] = watcher.time
            whole_data['id'] = watcher.id
            whole_data['hash_code'] = hash_code
            
            params_collection = cls.db['params']
            
            try:
                next(params_collection.find({"hash_code" : hash_code}))
                query = {"hash_code": {"$regex" : hash_code}}
                new_val = {"$set" : whole_data}
                params_collection.update_many(query, new_val)
            except StopIteration:
                params_collection.insert(whole_data)

            # Saving log to local storage
            # os.makedirs(save_path, exist_ok=True)
            # Logger.get_logger().debug("Saving json str {}".format(json_str))
            # json_str = json.dumps(whole_data)
            # name = watcher.name + '_' + hash_code + '_' + watcher.time
            # with open(save_path + '/{}.json'.format(name), 'w') as f:
            #     f.write(json_str)
            
    @classmethod
    def run_save(cls):
        if hasattr(cls, 'save_proc'):
            Logger.get_logger().warning("Already have one saving process...")
            return False
        Logger.get_logger().info("Starting saving process...")
        cls.save_proc = Process(target=cls.save_to_file)
        # save_proc.daemon = True 
        # Cannot set save process to daemon, otherwise save process will interupt once main thread exits.
        cls.save_proc.start()
        return True
    
    @classmethod
    def terminate_save_proc(cls):
        if cls.save_proc:
            Logger.get_logger().warning("Saving process will terminate in 5s...")
            time.sleep(5)
            remain_wait_round = 10
            while not cls.WATCHER_QUEUE.empty():
                Logger.get_logger().warning("Queue is not empty, waiting save_proc to finish remain queue tasks")
                time.sleep(2)
                if remain_wait_round == 0:
                    break
                remain_wait_round -= 1
            cls.save_proc.terminate()
            Logger.get_logger().info("Closing saving process...")
            return True
        else:
            Logger.get_logger().warning("No saving process can be terminated...")
            return False
    
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'WATCHER_QUEUE'):
            cls.WATCHER_QUEUE = Queue()
            cls.run_save()
        return super().__new__(cls)

    def __init__(self, name):
        self.model_parameters = dict()
        self.training_parameters = dict()
        self.miscellaneous_parameters = dict()
        self.data_parameters = dict()
        self.models = dict()
        self.results = dict()
        self.id = get_md5_hash(name + f'{time.time()}')
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.name = name
        self.description = name

    def insert_model_parameters(self, key, value):
        self.model_parameters[key] = value
    
    def insert_training_parameters(self, key, value):
        self.training_parameters[key]
    
    def insert_miscellaneous_parameters(self, key, value):
        self.miscellaneous_parameters[key] = value
    
    def insert_data_parameters(self, key, value):
        self.data_parameters[key] = value
    
    def get_model_parameter_by_key(self, key):
        return self.model_parameters[key]
    
    def get_training_parameter_by_key(self, key):
        return self.training_parameters[key]
    
    def get_miscellaneous_parameter_by_key(self, key):
        return self.miscellaneous_parameters[key]

    def get_data_parameter_by_key(self, key):
        return self.data_parameters[key]

    def delete_model_parameter_by_key(self, key):
        self.model_parameters.pop(key)

    def delete_training_parameter_by_key(self, key):
        self.training_parameters.pop(key)

    def delete_miscellaneous_parameter_by_key(self, key):
        self.miscellaneous_parameters.pop(key)

    def delete_data_parameter_by_key(self, key):
        self.data_parameters.pop(key) 

    def update_model_parameter_by_key(self, key, value):
        self.model_parameters[key] = value

    def update_training_parameter_by_key(self, key, value):
        self.training_parameters[key] = value

    def update_miscellaneous_parameter_by_key(self, key, value):
        self.miscellaneous_parameters[key] = value
    
    def update_data_parameter_by_key(self, key, value):
        self.data_parameters[key] = value

if __name__ == '__main__':
    x = ParameterWatcher('test')
    pkgs1 = [{'parameter_type': ParameterType.MODEL, 'operation_type': ParameterHandlerOperation.INSERT, 'insert_keys':['time'], 'time': [100, 200, 300]} for i in range(100)]
    pkgs2 = [{'parameter_type': ParameterType.DATA, 'operation_type': ParameterHandlerOperation.INSERT, 'insert_keys':['time'], 'time': [100, 200, 300]} for i in range(100)]
    pkgs3 = [{'parameter_type': ParameterType.TRANINING, 'operation_type': ParameterHandlerOperation.INSERT, 'insert_keys':['time'], 'time': [100, 200, 300]} for i in range(100)]
    for pkgs in [pkgs1, pkgs2, pkgs3]:
        for pkg in pkgs:
            x.main_parameter_handler(pkg)
    # time.sleep(5)
    ParameterWatcher.terminate_save_proc()