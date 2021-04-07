version_infor = '''
* File: pyp3d.py
* Brief: BIMBase-Python SDK
* Version: 2.0.11
* Date: 2020.04.07
'''
print(version_infor)
from multiprocessing import shared_memory
import numpy                            # 线性代数库
import pywintypes                       # win32异常
from win32 import win32pipe, win32file  # win32管道
from types import MethodType            # 成员方法
from types import FunctionType          # 函数类型
from functools import partial           # 偏函数
from functools import wraps             # 装饰器修复函数
import tkinter                          # python自带界面
import os                               # 截取路径
import sys                              # 添加路径
import math                             # 数学库
import atexit                           # 退出模块时清理资源
import threading                        # 线程
import copy                             # 深拷贝
import time                             # 休眠
import struct                           # 序列化
import imp

# 自带库
# 外部依赖库
# win32库可以更换通讯方案，自己写，numpy仅涉及矩阵相关运算，也可以自己写
###############################################################################
#                                   常数                                      #
###############################################################################
pi = numpy.pi
sleep_time = 0.00001
###############################################################################
#                                序列化接口                                    #
###############################################################################


def _push_dict(value: dict):
    s = _Stack()
    for k, v in value.items():
        s.push(v)
        s.buffer += _reflection_pack[type(v)]
        s.push(k)
    return s.buffer + struct.pack('Q', len(value))


def _pop_dict(s):
    result = dict()
    size = struct.unpack('Q', s._pop(8))[0]
    for _ in range(size):
        k = s.pop(str)
        describe = s.pop(str)
        result[k] = s.pop(_reflection_unpack[describe])
    return result


def _push_list(value: list):
    s = _Stack()
    for v in value[::-1]:
        s.push(v)
        if issubclass(type(v), P3DData):
            s.buffer += _reflection_pack[P3DData]
        else:
            s.buffer += _reflection_pack[type(v)]
    return s.buffer + struct.pack('Q', len(value))


def _pop_list(s):
    result = list()
    size = struct.unpack('Q', s._pop(8))[0]
    for _ in range(size):
        describe = s.pop(str)
        result.append(s.pop(_reflection_unpack[describe]))
    return result


def _prefix(buf):
    return buf + struct.pack('Q', len(buf))


_reflection_serialize = {
    bool: lambda x: struct.pack('?', x),
    int: lambda x: struct.pack('q', x),
    float: lambda x: struct.pack('d', x),
    str: lambda x: _prefix(x.encode(encoding='GBK')),
    bytes: lambda x: _prefix(x),
    dict:   _push_dict,
    list:   _push_list,
}
_reflection_pop = {
    bool: lambda x: struct.unpack('?', x._pop(1))[0],
    int: lambda x: struct.unpack('q', x._pop(8))[0],
    float: lambda x: struct.unpack('d', x._pop(8))[0],
    str: lambda x: x._pop(struct.unpack('Q', x._pop(8))[0]).decode(encoding='GBK'),
    bytes: lambda x: x._pop(struct.unpack('Q', x._pop(8))[0]),
    dict: lambda x: _pop_dict(x),
    list: lambda x: _pop_list(x),
}
_reflection_pack = {
    bool:   _prefix('bool'.encode(encoding='GBK')),
    int:    _prefix('__int64'.encode(encoding='GBK')),
    float:  _prefix('double'.encode(encoding='GBK')),
    str:    _prefix('class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >'.encode(encoding='GBK')),
    bytes:  _prefix('class std::vector<unsigned char,class std::allocator<unsigned char> >'.encode(encoding='utf-8')),
    dict:   _prefix('class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class python::PythonObject,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class python::PythonObject> > >'.encode(encoding='GBK')),
    list:   _prefix('class std::vector<class python::PythonObject,class std::allocator<class python::PythonObject> >'.encode(encoding='GBK')),
}
_reflection_unpack = {
    'bool':                     bool,
    '__int64':                  int,
    'double':                   float,
    'class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >': str,
    'class std::vector<unsigned char,class std::allocator<unsigned char> >':                  bytes,
    'class std::map<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> >,class python::PythonObject,struct std::less<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > >,class std::allocator<struct std::pair<class std::basic_string<char,struct std::char_traits<char>,class std::allocator<char> > const ,class python::PythonObject> > >': dict,
    'class std::vector<class python::PythonObject,class std::allocator<class python::PythonObject> >': list,
}


class _Stack:
    '''
    字节栈
    '''

    def __init__(self, buffer: bytes = b''):
        self.buffer = copy.deepcopy(buffer)

    def push(self, value) -> None:
        if type(value) in _reflection_serialize:
            self.buffer += _reflection_serialize[type(value)](value)
        else:
            self.buffer += value._serialize()

    def pop(self, valueType):
        return _reflection_pop[valueType](self)

    def _pop(self, length):
        if len(self.buffer) < length:
            raise ValueError('buffer长度不足')
        if length > 0:
            value = self.buffer[-length:]
            self.buffer = self.buffer[:-length]
        else:
            value = b''
        return value


BytesStack = _Stack


def _serialize(value):
    return _reflection_serialize[type(value)](value)
###############################################################################
#                                 通讯接口                                     #
###############################################################################


class Communication:
    '''
    通讯类,使用时可以选择成为客户端或服务端
    '''

    def __init__(self):
        self.hPipe = None

    def becomeServer(self, name: str):
        '''
        成为服务端
        '''
        try:
            self.hPipe = win32pipe.CreateNamedPipe(name, win32pipe.PIPE_ACCESS_DUPLEX,
                                                   win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE, 1, 0, 0,
                                                   win32pipe.NMPWAIT_WAIT_FOREVER, None)
        except pywintypes.error as e:
            print(e)
            raise pywintypes.error(e)

    def connect(self):
        '''
        成为服务端后调用, 阻塞等待客户端连接
        '''
        win32pipe.ConnectNamedPipe(self.hPipe, None)

    def disconnect(self):
        '''
        成为服务端后调用, 用于断开连接
        '''
        win32pipe.DisconnectNamedPipe(self.hPipe)

    def becomeClient(self, name: str):
        '''
        成为客户端, 无法阻塞BUG
        '''
        splitPos = name.rfind('\\')
        memName = name[splitPos+1:]
        while True:
            serverShareMem = shared_memory.SharedMemory(name=memName)
            bytesMemory = serverShareMem.buf.tobytes()
            strMemory = bytesMemory[:1].decode(encoding='GBK')
            if strMemory == '1':
                break
        # 无法阻塞BUG,防止BIMBase那边两次函数间隔中奖
        time.sleep(sleep_time)
        self.hPipe = win32file.CreateFile(name, win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                                          0, None, win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)

    def receive(self) -> bytes:
        '''
        共用方法, 接收
        '''
        readSize = struct.unpack('L', win32file.ReadFile(
            self.hPipe, struct.calcsize('L'), None)[1])[0]
        if readSize == 0:
            return b''
        else:
            return win32file.ReadFile(self.hPipe, readSize, None)[1]

    def send(self, buf: bytes = b''):
        '''
        共用方法, 发送
        '''
        if not isinstance(buf, bytes):
            raise TypeError('只能发送二进制串')
        win32file.WriteFile(self.hPipe, struct.pack('L', len(buf))+buf)

    def close(self):
        '''
        共有方法, 关闭句柄
        '''
        win32file.CloseHandle(self.hPipe)
        self.hPipe = None


serviceName = '\\\\.\\Pipe\\pyp3ddebug'
createThumbOrProp = 'NoCreate'
if len(sys.argv) > 1:
    serviceName = sys.argv[1]
    print(serviceName)
    createThumbOrProp = sys.argv[1]


class PyP3DRuntime:
    _methods = {}  # 注册的方法

    class _ProcessingRequests(threading.Thread):
        '''
        响应来自P3D的请求的线程
        '''

        def __init__(self, name):
            threading.Thread.__init__(self)
            self.name = name
            self.life = True

        def run(self):
            communication1 = Communication()
            communication1.becomeClient(self.name)
            buf = _Stack(communication1.receive())
            name = buf.pop(str)
            try:
                args = buf.pop(list)
                if name in PyP3DRuntime._methods:
                    fun = PyP3DRuntime._methods[name]
                    reslut = fun(*args)
                else:
                    reslut = []
                if isinstance(reslut, tuple):
                    reslut = list(reslut)
                else:
                    reslut = [reslut, ]
            except Exception as e:
                print(e)
                reslut = []
            finally:
                communication2 = Communication()
                communication2.becomeServer(self.name)
                communication2.connect()
                communication2.send(_serialize(reslut))
            self.life = False

    _currentObject = None

    def register(obj):
        '''
        注册方法到Runtime
        '''
        if isinstance(obj, FunctionType):
            PyP3DRuntime._methods[obj.__name__] = obj
            return obj
        else:
            PyP3DRuntime._currentObject = obj
            for attrName in dir(obj):
                if attrName[0:2] == '__':
                    continue
                attr = getattr(obj, attrName)
                if not callable(attr):
                    continue
                PyP3DRuntime._methods[attr.__name__] = attr

    _toolLock = threading.Condition()

    def launchTool(toolObject=None, exitRuntime=True):
        '''
        触发Python工具
        '''
        if toolObject != None:
            if type(toolObject) == type:
                raise TypeError('launchTool需要的是对象,而不是类')
            PyP3DRuntime.register(toolObject)
        print('Enter tool.')
        PyP3DRuntime.startRuntime()
        callP3D('launchTool')
        if PyP3DRuntime._toolLock.acquire():
            PyP3DRuntime._toolLock.wait()
            PyP3DRuntime._toolLock.release()
        print('Exit tool.')
        if exitRuntime:
            PyP3DRuntime.stopRuntime()

    _runtimeServiceThread = None
    _operatorResponseServiceThread = None
    _operatorResponseServiceThreadDebug = None

    class _Runtime(threading.Thread):
        '''
        运行时线程
        '''

        def __init__(self, pipeName):
            threading.Thread.__init__(self)
            self.pipeName = pipeName
            self.runtimeServiceLife = False
            self.threadPool = []

        def stop(self):
            if not self.runtimeServiceLife:
                return
            self.runtimeServiceLife = False
            communicationP3dRuntimeQuit = Communication()
            communicationP3dRuntimeQuit.becomeClient(self.pipeName)
            communicationP3dRuntimeQuit.send(b'')
            communicationP3dRuntimeQuit.close()

        def run(self):
            print('RuntimeOperator started.')
            communicationRuntime = Communication()
            try:
                communicationRuntime.becomeServer(self.pipeName)
            except pywintypes.error:
                # 先消灭其他pyP3DRuntime, 只能有一个
                self.stop()
                communicationRuntime.becomeServer(self.pipeName)
            # 开启循环响应
            self.runtimeServiceLife = True
            while self.runtimeServiceLife:
                communicationRuntime.connect()
                # 清理线程池
                self.threadPool = list(
                    filter(lambda x: x.life, self.threadPool))
                # 添加新线程
                buf = communicationRuntime.receive()
                if not buf:
                    self.runtimeServiceLife = False
                self.threadPool.append(
                    PyP3DRuntime._ProcessingRequests(_Stack(buf).pop(str)))
                self.threadPool[-1].start()
                communicationRuntime.disconnect()
            communicationRuntime.close()
            print('Runtime exited.')

    def startRuntime():
        '''
        开启运行时线程
        '''
        if PyP3DRuntime._runtimeServiceThread is None or PyP3DRuntime._runtimeServiceThread.runtimeServiceLife == False:
            PyP3DRuntime._runtimeServiceThread = PyP3DRuntime._Runtime(
                serviceName)
            PyP3DRuntime._runtimeServiceThread.start()

    def stopRuntime():
        '''
        停止运行时线程
        '''
        if PyP3DRuntime._runtimeServiceThread is None or PyP3DRuntime._runtimeServiceThread.runtimeServiceLife == False:
            return
        PyP3DRuntime._runtimeServiceThread.stop()
        PyP3DRuntime._runtimeServiceThread.join()


def callP3D(methodName: str, *args):
    '''
    访问平台方法
    '''
    communicationP3dRuntime = Communication()
    communicationP3dRuntime.becomeClient(r"\\.\Pipe\P3DRuntime")
    pipeName = r"\\.\Pipe\pyP3DCall" + str(time.time())
    communicationRequest = Communication()
    communicationRequest.becomeServer(pipeName)
    communicationP3dRuntime.send(_serialize(pipeName))
    communicationRequest.connect()
    communicationRequest.send(_serialize(list(args)) + _serialize(methodName))
    buf = communicationRequest.receive()
    return _Stack(buf).pop(list)

###############################################################################
#                              Python数据接口                                  #
###############################################################################


class _Property:
    '''
    属性对象
    '''

    def __init__(self, value=None):
        self._value = value
        self._data = {
            'obvious': False,   # 外显属性
            'pivotal': True,   # 关键属性
            'readonly': False,  # 只读属性
            'personal': False,  # 个性化属性
            'show': False,  # 绘制属性
            'group': '',  # 分组
            'description': '',  # 属性描述
        }

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


sys.path.append('')


class _Operator:
    '''
    算子
    '''

    def __init__(self):
        self._this = P3DData()
        self._filePath = ''     # 会被拷贝到算子库
        self._methodName = ''   #

    def __call__(self, exePath=None):
        modulePath, fileName = os.path.split(self._filePath)
        if not exePath is None:
            index = modulePath.find('/PythonScript//ParamComponentLib')
            if index > 0:
                modulePath = exePath + modulePath[index:]
        moduleName, _ = os.path.splitext(fileName)
        sys.path.pop()
        sys.path.append(modulePath)
        g_mode = __import__(moduleName)
        imp.reload(g_mode)
        return getattr(g_mode, self._methodName)(self._this)

    def _serialize(self):
        s = _Stack()
        s.push(self._filePath)
        s.push(self._methodName)
        return s.buffer

    def _pop(self, s: _Stack):
        self._methodName = s.pop(str)
        self._filePath = s.pop(str)
        return self


_reflection_serialize[_Operator] = lambda x: x._serialize()
_reflection_pop[_Operator] = lambda x: _Operator()._pop(x)
_reflection_pack[_Operator] = _prefix(
    'class BPPython::PythonOperator'.encode(encoding='GBK'))
_reflection_unpack['class BPPython::PythonOperator'] = _Operator


@PyP3DRuntime.register
def _operator_callback(operator, data, exePath):
    operator._this = data
    operator(exePath)
    return operator._this


@PyP3DRuntime.register
def _test_valid():
    return True


class P3DData:
    '''
    PyP3D 数据类

    属性说明
    |    关键字    |    默认值    |    说明    |\n
    | value       | None         | 值        |\n
    | obvious     | False        | 外显属性   |\n
    | pivotal     | True         | 关键属性   |\n
    | readonly    | False        | 只读属性   |\n
    | personal    | False        | 个性化属性 |\n
    | show        | False        | 绘制属性   |\n
    | group       | ''           | 分组       |\n
    | description | ''           | 属性描述   |\n
    '''

    def __init__(self, data=dict()):  # map<string, object>  ->  map<string, DecorativeObject>
        self._data = {}  # str:_Property
        for k, v in data.items():
            self[k] = v
        self._data['\tNAME'] = _Property('')
        self._data['\tPREVIEW_VIEW'] = _Property('')

    def __str__(self):  # 日后再优化显示
        s = ''
        for k, v in self._data.items():
            s += k+'\t'+str(v.value)+'\n'
        return s

    def __getitem__(self, key):
        value = self._data[key].value
        if isinstance(value, _Operator):
            value._this = self
        return value

    def __setitem__(self, key, value):
        if not key in self._data:
            self._data[key] = _Property(None)
        if isinstance(value, FunctionType):
            self._data[key].value = _Operator()
            self._data[key].value._methodName = value.__name__
            self._data[key].value._filePath = __import__(
                value.__module__).__file__
            self._data[key].value._this = self
        elif isinstance(value, tuple):
            self._data[key].value = list(x)
        else:
            self._data[key].value = value

    def __delitem__(self, key):
        del self._data[key]

    def _serialize(self):
        s = _Stack()
        for k, prop in self._data.items():
            s.push(prop._data)
            s.push(prop._value)
            s.buffer += _reflection_pack[type(prop._value)]
            s.push(k)
        s.buffer += struct.pack('Q', len(self._data))
        return s.buffer

    def _pop(self, s):
        size = struct.unpack('Q', s._pop(8))[0]
        for _ in range(size):
            k = s.pop(str)
            describe = s.pop(str)
            if describe == '':
                describe = s.pop(str)
                continue
            self._data[k] = _Property()
            self._data[k]._value = s.pop(_reflection_unpack[describe])
            self._data[k]._data = s.pop(dict)
        return self

    def setup(self, key, **args):
        if key not in self._data:
            self._data[key] = _Property('')
        for vk, vv in args.items():
            self._data[key][vk] = vv
    # 构件名称

    @property
    def name(self):
        return self._data['\tNAME'].value

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._data['\tNAME'].value = value
        else:
            raise TypeError('不支持的类型')
    # 预览视角的变换矩阵

    def set_view(self, az, el):
        '''
        @az 方位角  
        @el 仰角  
        '''
        self._data['\tPREVIEW_VIEW'].value = rotation(Vec3(1, 0, 0), -el) * rotation(Vec3(0, 1, 0), -az) * rotation(
            Vec3(0, 0, 1), pi) * rotation(Vec3(0, 1, 0), pi) * rotation(Vec3(1, 0, 0), 0.5*pi)

    @property
    def view(self):
        return self._data['\tPREVIEW_VIEW'].value

    @view.setter
    def view(self, value):
        if isinstance(value, TransformationMatrix):
            self._data['\tPREVIEW_VIEW'].value = value
        else:
            raise TypeError('不支持的类型')
    # 更新方法

    @property
    def replaceMethod(self):
        return self._data['replace'].value

    @replaceMethod.setter
    def replaceMethod(self, value):
        if isinstance(value, FunctionType):
            self._data['replace'] = _Property('')
            self._data['replace'].value = _Operator()
            self._data['replace'].value._methodName = value.__name__
            self._data['replace'].value._filePath = __import__(
                value.__module__).__file__
            self._data['replace'].value._this = self
    # 动态预览方法

    @property
    def dynamicMethod(self):
        return self._data['\tPLACE_TOOL_OPERATOR_DYNAMIC']

    @dynamicMethod.setter
    def dynamicMethod(self, value):
        if isinstance(value, FunctionType):
            self._data['\tPLACE_TOOL_OPERATOR_DYNAMIC'] = _Property('')
            self._data['\tPLACE_TOOL_OPERATOR_DYNAMIC'].value = _Operator()
            self._data['\tPLACE_TOOL_OPERATOR_DYNAMIC'].value._methodName = value.__name__
            self._data['\tPLACE_TOOL_OPERATOR_DYNAMIC'].value._filePath = __import__(
                value.__module__).__file__
            self._data['\tPLACE_TOOL_OPERATOR_DYNAMIC'].value._this = self
    # 布置方法

    @property
    def placeMethod(self):
        return self._data['\tPLACE_TOOL_OPERATOR_PLACE'].value

    @placeMethod.setter
    def placeMethod(self, value):
        if isinstance(value, FunctionType):
            self._data['\tPLACE_TOOL_OPERATOR_PLACE'] = _Property('')
            self._data['\tPLACE_TOOL_OPERATOR_PLACE'].value = _Operator()
            self._data['\tPLACE_TOOL_OPERATOR_PLACE'].value._methodName = value.__name__
            self._data['\tPLACE_TOOL_OPERATOR_PLACE'].value._filePath = __import__(
                value.__module__).__file__
            self._data['\tPLACE_TOOL_OPERATOR_PLACE'].value._this = self
    # 动态预览以及布置时的捕捉点

    @property
    def capturedPoint(self):
        if '\tPLACE_TOOL_CAPTURED_POINT' in self._data:
            return self._data['\tPLACE_TOOL_CAPTURED_POINT'].value
        return None

    @capturedPoint.setter
    def capturedPoint(self, value):
        self._data['\tPLACE_TOOL_CAPTURED_POINT'] = _Property('')
        self._data['\tPLACE_TOOL_CAPTURED_POINT'].value = value
    # 动态预览绘制几何体

    @property
    def dynamicGeometry(self):
        if '\tPLACE_TOOL_DYNAMICALLY_DISPLAY' in self._data:
            return self._data['\tPLACE_TOOL_DYNAMICALLY_DISPLAY'].value

    @dynamicGeometry.setter
    def dynamicGeometry(self, value):
        self._data['\tPLACE_TOOL_DYNAMICALLY_DISPLAY'] = _Property('')
        self._data['\tPLACE_TOOL_DYNAMICALLY_DISPLAY'].value = value
    # 实例的变换矩阵

    @property
    def transformation(self):
        if '\tCASE_LOCAL_COORDINATE' in self._data:
            return self._data['\tCASE_LOCAL_COORDINATE'].value

    @transformation.setter
    def transformation(self, value):
        self._data['\tCASE_LOCAL_COORDINATE'] = _Property('')
        self._data['\tCASE_LOCAL_COORDINATE'].value = value
    # 布置结束标志

    @property
    def placeEnd(self):
        if '\tPLACE_TOOL_END_SIGN' in self._data:
            return self._data['\tPLACE_TOOL_END_SIGN'].value

    @placeEnd.setter
    def placeEnd(self, value):
        self._data['\tPLACE_TOOL_END_SIGN'] = _Property('')
        self._data['\tPLACE_TOOL_END_SIGN'].value = value
    # 线性构件长度

    @property
    def LinearComponentLengthKey(self):
        if '\tLinearComponentLength' in self._data:
            return self._data['\tLinearComponentLength'].value

    @LinearComponentLengthKey.setter
    def LinearComponentLengthKey(self, value):
        self._data['\tLinearComponentLength'] = _Property('')
        self._data['\tLinearComponentLength'].value = value


_reflection_serialize[P3DData] = lambda x: x._serialize()
_reflection_pop[P3DData] = lambda x: P3DData()._pop(x)
_reflection_pack[P3DData] = _prefix(
    'class python::PythonCombinedDecorativeObject'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonCombinedDecorativeObject'] = P3DData


def launchData(data: P3DData):
    data['replace']()
    global createThumbOrProp
    data[createThumbOrProp] = True
    callP3D('launchData', data)


def launchDataTemp(data: P3DData):
    data['replace']()
    callP3D('launchDataTemp', data)


def testLaunchData(*args):
    return callP3D('testLaunchData', *args)

###############################################################################
#                                几何数据接口                                  #
###############################################################################
# vec3与matrix通用数据结构


class PythonArray:
    def __init__(self):
        self._dimension = []
        self._data = []

    def _serialize(self):
        s = _Stack()
        for v in self._dimension[::-1]:
            s.push(v)
        s.buffer += struct.pack('Q', len(self._dimension))
        s.push(self._data)
        return s.buffer

    def _pop(self, s):
        self._data = s.pop(list)
        dimension_size = struct.unpack('Q', s._pop(8))[0]
        for i in range(dimension_size):
            self._dimension.append(struct.unpack('Q', s._pop(8))[0])
        if not isinstance(self._data[0], float):
            return self
        if self._dimension[0] == 4 and self._dimension[1] == 4:  # 矩阵
            matrix = numpy.array(self._data)
            matrix = matrix.reshape(4, 4)
            # matrix = numpy.row_stack((matrix, numpy.array([0, 0, 0, 1])))
            return TransformationMatrix(matrix)
        elif self._dimension[0] == 3 and self._dimension[1] == 1:  # 向量
            return Vec3(self._data[0], self._data[1], self._data[2])
        else:
            return self


_reflection_serialize[PythonArray] = lambda x: x._serialize()
_reflection_pop[PythonArray] = lambda x: PythonArray()._pop(x)
_reflection_pack[PythonArray] = _prefix(
    'class python::PythonArray'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonArray'] = PythonArray
# 坐标点


class Vec3:
    '''
    三维矢量（列矢量）
    '''

    def __init__(self, *args):
        if len(args) == 0:
            self.vector = numpy.array([[0], [0], [0], [1]])
        elif len(args) == 1:
            if isinstance(args[0], numpy.ndarray):
                if args[0].shape != (4, 1):
                    raise ValueError('shape不匹配')
                else:
                    self.vector = args[0]
            elif isinstance(args[0], list) or isinstance(args[0], tuple):
                if len(args[0]) != 3:
                    raise ValueError('构造三维矢量需要3个分量')
                self.vector = numpy.array(
                    [[args[0][0]], [args[0][1]], [args[0][2]], [1]])
            else:
                raise ValueError('不支持的类型')
        elif len(args) == 3:
            self.vector = numpy.array([[args[0]], [args[1]], [args[2]], [1]])
        else:
            raise ValueError('不合适的参数')

    def __str__(self):
        return str((self.x, self.y, self.z))

    def _serialize(self):
        pythonArray = PythonArray()
        pythonArray._dimension = [3, 1]
        pythonArray._data = [self.x, self.y, self.z]
        buffer = pythonArray._serialize()
        return buffer

    @property
    def x(self):
        return float(self.vector[0][0])

    @x.setter
    def x(self, value):
        self.vector[0][0] = value

    @property
    def y(self):
        return float(self.vector[1][0])

    @y.setter
    def y(self, value):
        self.vector[1][0] = value

    @property
    def z(self):
        return float(self.vector[2][0])

    @z.setter
    def z(self, value):
        self.vector[2][0] = value

    def __add__(self, b):
        if isinstance(b, Vec3):
            return Vec3(self.vector + b.vector)
        else:
            raise TypeError('不合适的参数')

    def __radd__(self, a):
        if isinstance(a, Vec3):
            return Vec3(a.vector + self.vector)
        else:
            raise TypeError('不合适的参数')

    def __sub__(self, b):
        if isinstance(b, Vec3):
            return Vec3(self.vector - b.vector)
        else:
            raise TypeError('不合适的参数')

    def __rsub__(self, a):
        if isinstance(a, Vec3):
            return Vec3(a.vector - self.vector)
        else:
            raise TypeError('不合适的参数')

    def __mul__(self, b):
        if isinstance(b, float) or isinstance(b, int):
            return Vec3(self.vector * b)
        else:
            raise TypeError('不合适的参数')

    def __rmul__(self, a):
        if isinstance(a, float) or isinstance(a, int):
            return Vec3(a * self.vector)
        else:
            raise TypeError('不合适的参数')


_reflection_serialize[Vec3] = lambda x: x._serialize()
_reflection_pack[Vec3] = _prefix(
    'class python::PythonArray'.encode(encoding='GBK'))


def norm(vec: Vec3):
    '''
    计算模长（二范数）
    '''
    return float(numpy.linalg.norm(vec.vector[0:3]))


def unitize(vec: Vec3):
    '''
    计算单位矢量
    '''
    if (vec.vector[0:3] == numpy.zeros(3)).all():
        raise ValueError('零向量没有单位向量')
    return Vec3(vec.vector/norm(vec))


def linspace(a, b, n):
    '''
    产生线性分布
    '''
    if isinstance(a, Vec3) and isinstance(b, Vec3):
        return [Vec3(x, y, z) for (x, y, z) in
                zip(numpy.linspace(a.x, b.x, n), numpy.linspace(a.y, b.y, n), numpy.linspace(a.z, b.z, n))]
    elif (isinstance(a, int) or isinstance(a, float)) and (isinstance(b, int) or isinstance(b, float)):
        return list(numpy.linspace(a, b, n))
    else:
        raise TypeError('不合适的参数')


def dot(a: Vec3, b: Vec3):
    '''
    矢量点积
    '''
    va = a.vector[0:3].T
    vb = b.vector[0:3]
    v = float(va.dot(vb))
    return float(a.vector[0:3].T.dot(b.vector[0:3]))


def cross(a: Vec3, b: Vec3):
    '''
    矢量叉积
    '''
    return Vec3(numpy.hstack((numpy.cross(a.vector[0:3].T, b.vector[0:3].T), [[0]])).T)

# 变换矩阵


class TransformationMatrix:
    '''
    线性变换矩阵 
    '''

    def __init__(self, *args):
        if len(args) == 0:
            self.matrix = numpy.identity(4)
        elif len(args) == 1 and isinstance(args[0], numpy.ndarray):
            if args[0].shape != (4, 4):
                ValueError('shape不匹配')
            else:
                self.matrix = args[0]

    def __str__(self):
        return str(self.matrix)

    def __mul__(self, b):
        if isinstance(b, TransformationMatrix):
            return TransformationMatrix(self.matrix.dot(b.matrix))
        elif isinstance(b, Vec3):
            return Vec3(self.matrix.dot(b.vector))
        elif isinstance(b, list):
            return self * combine(*b)
        elif isinstance(b, Geometry):
            c = copy.deepcopy(b)
            c._rmul(self)
            return c
        else:
            raise TypeError('不支持的类型')

    def _serialize(self):
        pythonArray = PythonArray()
        pythonArray._dimension = [4, 4]
        temp = self.matrix.tolist()
        pythonArray._data = [float(self.matrix[0][0]), float(self.matrix[0][1]), float(self.matrix[0][2]), float(self.matrix[0][3]),
                             float(self.matrix[1][0]), float(self.matrix[1][1]), float(
                                 self.matrix[1][2]), float(self.matrix[1][3]),
                             float(self.matrix[2][0]), float(self.matrix[2][1]), float(
                                 self.matrix[2][2]), float(self.matrix[2][3]),
                             float(self.matrix[3][0]), float(self.matrix[3][1]), float(self.matrix[3][2]), float(self.matrix[3][3])]
        buffer = pythonArray._serialize()
        return buffer

    @property
    def translation_part(self):
        return TransformationMatrix(self.matrix * numpy.array([[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]))

    @property
    def nontranslation_part(self):
        return TransformationMatrix(self.matrix * numpy.array([[1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0], [0, 0, 0, 1]]))


_reflection_serialize[TransformationMatrix] = lambda x: x._serialize()
_reflection_pack[TransformationMatrix] = _prefix(
    'class python::PythonArray'.encode(encoding='GBK'))


def translation(*args):
    '''
    产生平移矩阵
    '''
    if len(args) == 1 and isinstance(args[0], Vec3):
        return TransformationMatrix(numpy.array([[1, 0, 0, args[0].x], [0, 1, 0, args[0].y], [0, 0, 1, args[0].z], [0, 0, 0, 1]]))
    elif len(args) == 3:
        return TransformationMatrix(numpy.array([[1, 0, 0, args[0]], [0, 1, 0, args[1]], [0, 0, 1, args[2]], [0, 0, 0, 1]]))
    else:
        raise TypeError('不支持的类型')


def rotation(v: Vec3, angle: float):
    '''
    产生旋转矩阵（弧度制）
    '''
    nv = unitize(v)
    # Rodrigues' rotation formula
    M = numpy.array([[0, -nv.z, nv.y], [nv.z, 0, -nv.x], [-nv.y, nv.x, 0]])
    R = numpy.identity(3) + numpy.sin(angle)*M + (1-numpy.cos(angle))*M.dot(M)
    return TransformationMatrix(numpy.vstack((numpy.hstack((R, [[0], [0], [0]])), [0, 0, 0, 1])))


# def scaling(x, y, z):
#     '''
#     产生缩放矩阵
#     '''
#     return numpy.array([[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])

# 几何数据接口


class Geometry:
    '''
    几何对象(方便类型判断,防止用户将其他类型数据放到几何里面)
    '''

    def __init__(self):
        self._name = ''
        self._para = []
        self._negative = False  # 负几何体
        self._color = PythonColor(1, 1, 1, 1)
        self._matrix = TransformationMatrix()

    def _serialize(self, s):
        s.push(self._matrix)
        s.push(self._color)

    def _pop(self, s):
        self._color = s.pop(PythonColor)
        self._matrix = s.pop(PythonArray)

    def _rmul(self, a):
        self._matrix = a * self._matrix

    def __sub__(self, b):
        """
        布尔减 
        """
        return substract(self, b)

    def __add__(self, b):
        """
        布尔并
        """
        if self._name == 'unite':
            self._para.append(b)
            return self
        else:
            return unite(self, b)

    def __neg__(self):
        self._negative = not self._negative
        return self

    def __pos__(self):
        return self

    def __abs__(self):
        self._negative = False
        return self

    def __invert__(self):
        self._negative = not self._negative
        return self

    def color(self, *args):
        if len(args) == 1:
            if isinstance(args[0], PythonColor):
                self._color = args[0]
            elif isinstance(args[0], tuple) or isinstance(args[0], list):
                if len(args[0]) != 4:
                    raise ValueError('长度应该为4')
                self._color = PythonColor(
                    args[0][0], args[0][1], args[0][2], args[0][3])
        elif len(args) == 3:
            self._color = PythonColor(
                args[0], args[1], args[2], self._color[4])
        elif len(args) == 4:
            self._color = PythonColor(args[0], args[1], args[2], args[3])
        else:
            raise TypeError('不合适的参数')
        return self

    def _reflection_geometry(T):
        _reflection_serialize[T] = lambda x: x._serialize()
        _reflection_pop[T] = lambda x: Geometry()._pop(x)
        _reflection_pack[T] = _prefix(
            'class pyp3d::Geometry'.encode(encoding='GBK'))
        _reflection_unpack['class pyp3d::Geometry'] = Geometry
# Geometry._reflection_geometry(Geometry)


def createGeometry(geometry):
    '''
    创建纯几何
    '''
    if isinstance(geometry, Geometry):
        callP3D('createGeometry', geometry)
    elif isinstance(geometry, list):
        callP3D('createGeometry', combine(*geometry))


class GeometrySubstract(Geometry):
    def __init__(self):
        Geometry.__init__(self)
        self._name = 'substract'
        self._para = []

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        s.push(self._para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        self._para = s.pop(list)
        Geometry._pop(self, s)
        return self


_reflection_serialize[GeometrySubstract] = lambda x: x._serialize()
_reflection_pop[GeometrySubstract] = lambda x: GeometrySubstract()._pop(x)
_reflection_pack[GeometrySubstract] = _prefix(
    'class python::PythonGeometryVolumeBooleanSubstract'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeBooleanSubstract'] = GeometrySubstract

# 具体几何对象


def substract(a: Geometry, b: Geometry):
    '''
    布尔减
    '''
    geometry = GeometrySubstract()
    geometry._name = 'substract'
    geometry._para = [a, b]
    return geometry


class GeometryUnite(Geometry):
    def __init__(self):
        Geometry.__init__(self)
        self._name = 'unite'
        self._para = []

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        s.push(self._para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        self._para = s.pop(list)
        Geometry._pop(self, s)
        return self


_reflection_serialize[GeometryUnite] = lambda x: x._serialize()
_reflection_pop[GeometryUnite] = lambda x: GeometryUnite()._pop(x)
_reflection_pack[GeometryUnite] = _prefix(
    'class python::PythonGeometryVolumeBooleanUnite'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeBooleanUnite'] = GeometryUnite


def unite(*args):
    '''
    布尔并
    '''
    geometry = GeometryUnite()
    geometry._name = 'unite'
    geometry._para = list(args)
    return geometry


class GeometryIntersection(Geometry):
    def __init__(self):
        Geometry.__init__(self)
        self._name = 'intersection'
        self._para = []

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        s.push(self._para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        self._para = s.pop(list)
        Geometry._pop(self, s)
        return self


_reflection_serialize[GeometryIntersection] = lambda x: x._serialize()
_reflection_pop[GeometryIntersection] = lambda x: GeometryIntersection()._pop(x)
_reflection_pack[GeometryIntersection] = _prefix(
    'class python::PythonGeometryVolumeBooleanIntersection'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeBooleanIntersection'] = GeometryIntersection


def intersection(*args):
    '''
    布尔交
    '''
    geometry = GeometryIntersection()
    geometry._name = 'intersection'
    geometry._para = list(args)
    return geometry


class GeometryCombine(Geometry):
    def __init__(self):
        Geometry.__init__(self)
        self._name = 'combine'
        self._para = []

    def _serialize(self):
        s = _Stack()
        s.push(self._matrix)
        s.push(self._para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        self._para = s.pop(list)
        self._matrix = s.pop(PythonArray)
        return self

    def color(self, *args):
        if len(args) == 1:
            if isinstance(args[0], PythonColor):
                self._color = args[0]
                for para in self._para:
                    para.color(args[0])
            elif isinstance(args[0], tuple) or isinstance(args[0], list):
                if len(args[0]) != 4:
                    raise ValueError('长度应该为4')
                self._color = PythonColor(
                    args[0][0], args[0][1], args[0][2], args[0][3])
                for para in self._para:
                    para.color(args[0][0], args[0][1], args[0][2], args[0][3])
        elif len(args) == 3:
            self._color = PythonColor(
                args[0], args[1], args[2], self._color[4])
            for para in self._para:
                para.color(args[0], args[1], args[2], self._color[4])
        elif len(args) == 4:
            self._color = PythonColor(args[0], args[1], args[2], args[3])
            for para in self._para:
                para.color(args[0], args[1], args[2], args[3])
        else:
            raise TypeError('不合适的参数')
        return self


_reflection_serialize[GeometryCombine] = lambda x: x._serialize()
_reflection_pop[GeometryCombine] = lambda x: GeometryCombine()._pop(x)
_reflection_pack[GeometryCombine] = _prefix(
    'class python::PythonGeometryCombine'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryCombine'] = GeometryCombine


def _mergeGeometry(combineGeometry, b):
    for par in combineGeometry._para:
        par._matrix = combineGeometry._matrix * par._matrix
    combineGeometry._matrix = TransformationMatrix()
    if isinstance(b, list) or isinstance(b, tuple):
        for bi in b:
            _mergeGeometry(combineGeometry, bi)
    elif isinstance(b, GeometryCombine):
        for par in b._para:
            par._matrix = b._matrix * par._matrix
        b._matrix = TransformationMatrix()
        for bi in b._para:
            _mergeGeometry(combineGeometry, bi)
    else:
        combineGeometry._para.append(b)


def combine(*args):
    '''
    组合而不做布尔
    '''
    geometryCombine = GeometryCombine()
    geometryCombine._name = 'combine'
    _mergeGeometry(geometryCombine, args)
    return geometryCombine


class Sphere(Geometry):
    '''
    球体
    '''

    def __init__(self, center: Vec3, radius: float):
        Geometry.__init__(self)
        self._name = 'sphere'
        self._para = [Vec3(), 0.0]
        self.center = center
        self.radius = radius

    @property
    def center(self):
        return self._para[0]

    @center.setter
    def center(self, value):
        if isinstance(value, Vec3):
            self._para[0] = value
        else:
            self._para[0] = Vec3(value)

    @property
    def radius(self):
        return self._para[1]

    @radius.setter
    def radius(self, value):
        if isinstance(value, float):
            self._para[1] = value
        elif isinstance(value, int):
            self._para[1] = float(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        for para in self._para[::-1]:
            s.push(para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()

        self._para.append(s.pop(PythonArray))
        self._para.append(s.pop(float))

        Geometry._pop(self, s)
        return self


_reflection_serialize[Sphere] = lambda x: x._serialize()
_reflection_pop[Sphere] = lambda x: Sphere(Vec3(), 0.0)._pop(x)
_reflection_pack[Sphere] = _prefix(
    'class python::PythonGeometryVolumeSphere'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeSphere'] = Sphere


class Cone(Geometry):
    '''
    圆锥台
    '''

    def __init__(self, centerA: Vec3, centerB: Vec3, radiusA: float, radiusB: float = None):
        Geometry.__init__(self)
        self._name = 'cone'
        self._para = [Vec3(), Vec3(), 0.0, 0.0]
        self.centerA = centerA
        self.centerB = centerB
        self.radiusA = radiusA
        if radiusB:
            self.radiusB = radiusB
        else:
            self.radiusB = radiusA

    @property
    def centerA(self):
        return self._para[0]

    @centerA.setter
    def centerA(self, value):
        if isinstance(value, Vec3):
            self._para[0] = value
        else:
            self._para[0] = Vec3(value)

    @property
    def centerB(self):
        return self._para[1]

    @centerB.setter
    def centerB(self, value):
        if isinstance(value, Vec3):
            self._para[1] = value
        else:
            self._para[1] = Vec3(value)

    @property
    def radiusA(self):
        return self._para[2]

    @radiusA.setter
    def radiusA(self, value):
        if isinstance(value, float):
            self._para[2] = value
        elif isinstance(value, int):
            self._para[2] = float(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def radiusB(self):
        return self._para[3]

    @radiusB.setter
    def radiusB(self, value):
        if isinstance(value, float):
            self._para[3] = value
        elif isinstance(value, int):
            self._para[3] = float(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        for para in self._para[::-1]:
            s.push(para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        for _ in range(2):
            self._para.append(s.pop(PythonArray))
        for _ in range(2):
            self._para.append(s.pop(float))
        Geometry._pop(self, s)
        return self


_reflection_serialize[Cone] = lambda x: x._serialize()
_reflection_pop[Cone] = lambda x: Cone(Vec3(), Vec3(), 0.0)._pop(x)
_reflection_pack[Cone] = _prefix(
    'class python::PythonGeometryVolumeCone'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeCone'] = Cone


class TorusPipe(Geometry):
    '''
    环形管
    '''

    def __init__(self, center: Vec3, vectorX: Vec3, vectorY: Vec3, torusRadius: float,
                 pipeRadius: float, sweepAngle: float):
        Geometry.__init__(self)
        self._name = 'torusPipe'
        self._para = [Vec3(), Vec3(), Vec3(), 0.0, 0.0, 0]
        self.center = center
        self.vectorX = vectorX
        self.vectorY = vectorY
        self.majorRadius = torusRadius
        self.minorRadius = pipeRadius
        self.sweepAngle = sweepAngle

    @property
    def center(self):
        return self._para[0]

    @center.setter
    def center(self, value):
        if isinstance(value, Vec3):
            self._para[0] = value
        else:
            self._para[0] = Vec3(value)

    @property
    def vectorX(self):
        return self._para[1]

    @vectorX.setter
    def vectorX(self, value):
        if isinstance(value, Vec3):
            self._para[1] = value
        else:
            self._para[1] = Vec3(value)

    @property
    def vectorY(self):
        return self._para[2]

    @vectorY.setter
    def vectorY(self, value):
        if isinstance(value, Vec3):
            self._para[2] = value
        else:
            self._para[2] = Vec3(value)

    @property
    def majorRadius(self):
        return self._para[3]

    @majorRadius.setter
    def majorRadius(self, value):
        if isinstance(value, float):
            self._para[3] = value
        elif isinstance(value, int):
            self._para[3] = float(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def minorRadius(self):
        return self._para[4]

    @minorRadius.setter
    def minorRadius(self, value):
        if isinstance(value, float):
            self._para[4] = value
        elif isinstance(value, int):
            self._para[4] = float(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def sweepAngle(self):
        return self._para[5]

    @sweepAngle.setter
    def sweepAngle(self, value):
        if isinstance(value, float):
            self._para[5] = value
        elif isinstance(value, int):
            self._para[5] = float(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        for para in self._para[::-1]:
            s.push(para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        for _ in range(3):
            self._para.append(s.pop(PythonArray))
        for _ in range(3):
            self._para.append(s.pop(float))
        Geometry._pop(self, s)
        return self


_reflection_serialize[TorusPipe] = lambda x: x._serialize()
_reflection_pop[TorusPipe] = lambda x: TorusPipe(
    Vec3(), Vec3(), Vec3(), 0.0, 0.0, 0.0)._pop(x)
_reflection_pack[TorusPipe] = _prefix(
    'class python::PythonGeometryVolumeTorusPipe'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeTorusPipe'] = TorusPipe


class PythonColor:
    def __init__(self, r, g, b, a):
        self._color = [r, g, b, a]

    def _serialize(self):
        s = _Stack()
        for v in self._color[::-1]:
            s.push(float(v))
        return s.buffer

    def _pop(self, s):
        self._color.clear()
        for i in range(4):
            ele = s.pop(float)
            self._color.append(ele)
        return self


_reflection_serialize[PythonColor] = lambda x: x._serialize()
_reflection_pop[PythonColor] = lambda x: PythonColor(1, 1, 1, 1)._pop(x)
_reflection_pack[PythonColor] = _prefix(
    'class python::PythonColor'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonColor'] = PythonColor


class Box(Geometry):
    '''
    四棱台
    '''

    def __init__(self, baseOrigin: Vec3, topOrigin: Vec3, vectorX: Vec3, vectorY: Vec3,
                 baseX: float, baseY: float, topX: float, topY: float):
        Geometry.__init__(self)
        self._name = 'box'
        self._para = [Vec3(), Vec3(), Vec3(), Vec3(), 0.0, 0.0, 0.0, 0.0]
        self.baseOrigin = baseOrigin
        self.topOrigin = topOrigin
        self.vectorX = vectorX
        self.vectorY = vectorY
        self.baseX = baseX
        self.baseY = baseY
        self.topX = topX
        self.topY = topY

    @property
    def baseOrigin(self):
        return self._para[0]

    @baseOrigin.setter
    def baseOrigin(self, value):
        if isinstance(value, Vec3):
            self._para[0] = value
        else:
            self._para[0] = Vec3(value)

    @property
    def topOrigin(self):
        return self._para[1]

    @topOrigin.setter
    def topOrigin(self, value):
        if isinstance(value, Vec3):
            self._para[1] = value
        else:
            self._para[1] = Vec3(value)

    @property
    def vectorX(self):
        return self._para[2]

    @vectorX.setter
    def vectorX(self, value):
        if isinstance(value, Vec3):
            self._para[2] = value
        else:
            self._para[2] = Vec3(value)

    @property
    def vectorY(self):
        return self._para[3]

    @vectorY.setter
    def vectorY(self, value):
        if isinstance(value, Vec3):
            self._para[3] = value
        else:
            self._para[3] = Vec3(value)

    @property
    def baseX(self):
        return self._para[4]

    @baseX.setter
    def baseX(self, value):
        if isinstance(value, float):
            self._para[4] = value
        elif isinstance(value, int):
            self._para[4] = float(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def baseY(self):
        return self._para[5]

    @baseY.setter
    def baseY(self, value):
        if isinstance(value, float):
            self._para[5] = value
        elif isinstance(value, int):
            self._para[5] = float(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def topX(self):
        return self._para[6]

    @topX.setter
    def topX(self, value):
        if isinstance(value, float):
            self._para[6] = value
        elif isinstance(value, int):
            self._para[6] = float(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def topY(self):
        return self._para[7]

    @topY.setter
    def topY(self, value):
        if isinstance(value, float):
            self._para[7] = value
        elif isinstance(value, int):
            self._para[7] = float(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        for para in self._para[::-1]:
            s.push(para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        for _ in range(4):
            self._para.append(s.pop(PythonArray))
        for _ in range(4):
            self._para.append(s.pop(float))
        Geometry._pop(self, s)
        return self


_reflection_serialize[Box] = lambda x: x._serialize()
_reflection_pop[Box] = lambda x: Box(
    Vec3(), Vec3(), Vec3(), Vec3(), 0.0, 0.0, 0.0, 0.0)._pop(x)
_reflection_pack[Box] = _prefix(
    'class python::PythonGeometryVolumeBox'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeBox'] = Box


class Extrusion(Geometry):
    '''
    拉伸体 (直线放样)
    注意:points要求在同一平面
    '''

    def __init__(self, points: list, extrusionVector: Vec3):
        Geometry.__init__(self)
        self._name = 'extrusion'
        self._para = [[], Vec3()]
        self.points = points
        self.extrusionVector = extrusionVector

    @property
    def points(self):
        return self._para[0]

    @points.setter
    def points(self, value):
        if isinstance(value, list):
            self._para[0] = value
        elif isinstance(value, tuple):
            self._para[0] = list(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def extrusionVector(self):
        return self._para[1]

    @extrusionVector.setter
    def extrusionVector(self, value):
        if isinstance(value, Vec3):
            self._para[1] = value
        else:
            self._para[1] = Vec3(value)

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        s.push(self._para[0])
        s.push(self._para[1])  # 法向
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        vec = s.pop(PythonArray)
        point = s.pop(list)

        self._para.append(point)
        self._para.append(vec)

        Geometry._pop(self, s)
        return self


_reflection_serialize[Extrusion] = lambda x: x._serialize()
_reflection_pop[Extrusion] = lambda x: Extrusion([], Vec3())._pop(x)
_reflection_pack[Extrusion] = _prefix(
    'class python::PythonGeometryVolumeExtrusion'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeExtrusion'] = Extrusion


class RotationalSweep(Geometry):
    '''
    旋转扫描 (圆弧放样)
    '''

    def __init__(self, points: list, center: Vec3, axis: Vec3, sweepAngle: float):
        Geometry.__init__(self)
        self._name = 'rotationalSweep'
        self._para = [[], Vec3(), Vec3(), 0.0]
        self.points = points
        self.center = center
        self.axis = axis
        self.sweepAngle = sweepAngle

    @property
    def points(self):
        return self._para[0]

    @points.setter
    def points(self, value):
        if isinstance(value, list):
            self._para[0] = value
        elif isinstance(value, tuple):
            self._para[0] = list(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def center(self):
        return self._para[1]

    @center.setter
    def center(self, value):
        if isinstance(value, Vec3):
            self._para[1] = value
        else:
            self._para[1] = Vec3(value)

    @property
    def axis(self):
        return self._para[2]

    @axis.setter
    def axis(self, value):
        if isinstance(value, Vec3):
            self._para[2] = value
        else:
            self._para[2] = Vec3(value)

    @property
    def sweepAngle(self):
        return self._para[3]

    @sweepAngle.setter
    def sweepAngle(self, value):
        if isinstance(value, float):
            self._para[3] = value
        elif isinstance(value, float):
            self._para[3] = float(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        for para in self._para[::-1]:
            s.push(para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        self._para.append(s.pop(list))

        for _ in range(2):
            self._para.append(s.pop(PythonArray))
        self._para.append(s.pop(float))

        Geometry._pop(self, s)
        return self


_reflection_serialize[RotationalSweep] = lambda x: x._serialize()
_reflection_pop[RotationalSweep] = lambda x: RotationalSweep(
    [], Vec3(), Vec3(), 0.0)._pop(x)
_reflection_pack[RotationalSweep] = _prefix(
    'class python::PythonGeometryVolumeRotationalSweep'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeRotationalSweep'] = RotationalSweep


class RuledSweep(Geometry):
    '''
    直纹扫描
    '''

    def __init__(self, points1: list, points2: list):
        Geometry.__init__(self)
        self._name = 'ruledSweep'
        self._para = [[], []]
        self.points1 = points1
        self.points2 = points2

    @property
    def points1(self):
        return self._para[0]

    @points1.setter
    def points1(self, value):
        if isinstance(value, list):
            self._para[0] = value
        elif isinstance(value, tuple):
            self._para[0] = list(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def points2(self):
        return self._para[1]

    @points2.setter
    def points2(self, value):
        if isinstance(value, list):
            self._para[1] = value
        elif isinstance(value, tuple):
            self._para[1] = list(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        for para in self._para[::-1]:
            s.push(para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        for _ in range(2):
            self._para.append(s.pop(list))
        Geometry._pop(self, s)
        return self

_reflection_serialize[RuledSweep] = lambda x: x._serialize()
_reflection_pop[RuledSweep] = lambda x: RuledSweep([], [])._pop(x)
_reflection_pack[RuledSweep] = _prefix(
    'class python::PythonGeometryVolumeRuledSweep'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeRuledSweep'] = RuledSweep


class RuledSweepPlus(Geometry):
    '''
    直纹扫描
    '''
    def __init__(self, contours: list):
        Geometry.__init__(self)
        self._para = [[]]
        self.contours = contours

    @property
    def contours(self):
        return self._para[0]

    @contours.setter
    def contours(self, value):
        if isinstance(value, list):
            self._para[0] = value
        elif isinstance(value, tuple):
            self._para[0] = list(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        for para in self._para[0][::-1]:
            s.push(para)
        return s.buffer + struct.pack('Q', len(self._para[0]))

    def _pop(self, s):
        self._para[0].clear()
        size = struct.unpack('Q', s._pop(8))[0]
        for _ in range(size):
            self._para[0].append(s.pop(list))
        Geometry._pop(self, s)
        return self

_reflection_serialize[RuledSweepPlus] = lambda x: x._serialize()
_reflection_pop[RuledSweepPlus] = lambda x: RuledSweepPlus([])._pop(x)
_reflection_pack[RuledSweepPlus] = _prefix(
    'class python::PythonGeometryVolumeRuledSweepPlus'.encode(encoding='GBK'))
_reflection_unpack['class python::PythonGeometryVolumeRuledSweepPlus'] = RuledSweepPlus


class FilletPipe(GeometryCombine):
    '''
    圆角管 (圆管拐点间使用环形管连接)
    P0-None   P3-R3______P4-R4   P7-None
           \______/      \______/  
          P1-R1  P2-R2  P5-R5  P6-R6
    '''

    def __init__(self, points: list, filletRadius: list, pipeRadius: float):
        Geometry.__init__(self)
        if len(points) != len(filletRadius):
            raise ValueError('圆角半径数量与节点数量不一致')
        self._name = 'combine'  # 'unite'
        self._para = []
        point_start = points[0]
        for i in range(1, len(points)-1):
            vector_front = unitize(points[i-1] - points[i])
            vector_after = unitize(points[i+1] - points[i])
            sin_theta = math.sqrt(0.5*(1.0-dot(vector_front, vector_after)))
            theta = math.asin(sin_theta)
            fillet_range = filletRadius[i] / math.tan(theta)
            self._para.append(
                Cone(point_start, points[i] + fillet_range*vector_front, pipeRadius, pipeRadius))
            point_start = points[i] + fillet_range*vector_after
            vector_normal = vector_front + vector_after
            if norm(vector_normal) == 0:
                continue
            point_center = points[i] + \
                (filletRadius[i]/sin_theta) * unitize(vector_normal)
            vector_x = unitize(point_start-point_center)
            vector_y = unitize(
                cross(cross(vector_front, vector_after), vector_x))
            self._para.append(TorusPipe(
                point_center, vector_x, vector_y, filletRadius[i], pipeRadius, numpy.pi-2*theta))
        self._para.append(
            Cone(point_start, points[-1], pipeRadius, pipeRadius))


# Geometry._reflection_geometry(FilletPipe)
_reflection_serialize[FilletPipe] = lambda x: x._serialize()
_reflection_pack[FilletPipe] = _prefix(
    'class python::PythonGeometryCombine'.encode(encoding='GBK'))


class LineString(Geometry):
    '''
    多段线
    '''

    def __init__(self, points: list):
        Geometry.__init__(self)
        self._name = 'LineString'
        self._para = [[]]
        self.points = points

    @property
    def points(self):
        return self._para[0]

    @points.setter
    def points(self, value):
        if isinstance(value, list):
            self._para[0] = value
        elif isinstance(value, tuple):
            self._para[0] = list(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        s.push(self._para[0])
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        self._para.append(s.pop(list))
        return self


_reflection_serialize[LineString] = lambda x: x._serialize()
_reflection_pop[LineString] = lambda x: LineString([])._pop(x)
_reflection_pack[LineString] = _prefix(
    'class python::BPPythonGeometryContourLineExtrusionPlusString'.encode(encoding='GBK'))
_reflection_unpack['class python::BPPythonGeometryContourLineExtrusionPlusString'] = LineString


class Ellipse(Geometry):
    '''
    椭圆
    '''

    def __init__(self, center: Vec3, vector0: Vec3, vector90: Vec3, start: float, sweep: float):
        Geometry.__init__(self)
        self._name = 'Ellipse3d'
        self._para = [Vec3(), Vec3(), Vec3(), 0.0, 0.0]
        self.center = center
        self.vector0 = vector0
        self.vector90 = vector90
        self.start = start
        self.sweep = sweep

    @property
    def center(self):
        return self._para[0]

    @center.setter
    def center(self, value):
        if isinstance(value, Vec3):
            self._para[0] = value
        else:
            self._para[0] = Vec3(value)

    @property
    def vector0(self):
        return self._para[1]

    @vector0.setter
    def vector0(self, value):
        if isinstance(value, Vec3):
            self._para[1] = value
        else:
            self._para[1] = Vec3(value)

    @property
    def vector90(self):
        return self._para[2]

    @vector90.setter
    def vector90(self, value):
        if isinstance(value, Vec3):
            self._para[2] = value
        else:
            self._para[2] = Vec3(value)

    @property
    def start(self):
        return self._para[3]

    @start.setter
    def start(self, value):
        if isinstance(value, float):
            self._para[3] = value
        elif isinstance(value, int):
            self._para[3] = float(value)
        else:
            raise TypeError('不适合的参数')

    @property
    def sweep(self):
        return self._para[4]

    @sweep.setter
    def sweep(self, value):
        if isinstance(value, float):
            self._para[4] = value
        elif isinstance(value, int):
            self._para[4] = float(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        for para in self._para[::-1]:
            s.push(para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        self._para.append(s.pop(PythonArray))
        self._para.append(s.pop(PythonArray))
        self._para.append(s.pop(PythonArray))
        self._para.append(s.pop(float))
        self._para.append(s.pop(float))
        return self


_reflection_serialize[Ellipse] = lambda x: x._serialize()
_reflection_pop[Ellipse] = lambda x: Ellipse(
    Vec3(), Vec3(), Vec3(), 0.0, 0.0)._pop(x)
_reflection_pack[Ellipse] = _prefix(
    'class python::BPPythonGeometryContourLineExtrusionPlusEllipse'.encode(encoding='GBK'))
_reflection_unpack['class python::BPPythonGeometryContourLineExtrusionPlusEllipse'] = Ellipse


class ContourLine(Geometry):
    '''
    轮廓线（包含多线段和椭圆）
    '''

    def __init__(self, curves: list):
        Geometry.__init__(self)
        self._name = 'CurveArray'
        self._para = [[]]
        self.curves = curves

    def _rmul(self, a):
        if isinstance(a, TransformationMatrix):
            for i in range(len(self._para[0])):
                self._para[0][i] = a * self._para[0][i]

    @property
    def curves(self):
        return self._para[0]

    @curves.setter
    def curves(self, value):
        if isinstance(value, list):
            self._para[0] = value
        elif isinstance(value, tuple):
            self._para[0] = list(value)
        else:
            raise TypeError('不适合的参数')

    def _serialize(self):
        s = _Stack()
        s.push(self._para[0])
        return s.buffer

    def _pop(self, s):
        self._para.clear()
        self._para.append(s.pop(list))
        return self


_reflection_serialize[ContourLine] = lambda x: x._serialize()
_reflection_pop[ContourLine] = lambda x: ContourLine([])._pop(x)
_reflection_pack[ContourLine] = _prefix(
    'class python::BPPythonGeometryContourLineExtrusionPlus'.encode(encoding='GBK'))
_reflection_unpack['class python::BPPythonGeometryContourLineExtrusionPlus'] = ContourLine


class ExtrusionPlus(Geometry):
    '''
    复杂拉伸体
    '''

    def __init__(self, contourLine: list, extrusionVector: Vec3):
        Geometry.__init__(self)
        self._name = 'extrusionPlus'
        self._para = [[], Vec3()]
        self.contourLine = contourLine
        self.extrusionVector = extrusionVector

    @property
    def contourLine(self):
        return self._para[0]

    @contourLine.setter
    def contourLine(self, value):
        if isinstance(value, list):
            self._para[0] = value
        else:
            raise TypeError('不适合的参数')
        for line in value:
            if not isinstance(line, ContourLine):
                raise TypeError('复杂拉伸体 第一个参数：contourLine 不适合的参数')

    @property
    def extrusionVector(self):
        return self._para[1]

    @extrusionVector.setter
    def extrusionVector(self, value):
        if isinstance(value, Vec3):
            self._para[1] = value
        else:
            self._para[1] = Vec3(value)

    def _serialize(self):
        s = _Stack()
        Geometry._serialize(self, s)
        for para in self._para[::-1]:
            s.push(para)
        return s.buffer

    def _pop(self, s):
        self._para.clear()

        self._para.append(s.pop(list))
        self._para.append(s.pop(PythonArray))

        Geometry._pop(self, s)
        return self


# Geometry._reflection_geometry(ExtrusionPlus)
_reflection_serialize[ExtrusionPlus] = lambda x: x._serialize()
_reflection_pop[ExtrusionPlus] = lambda x: ExtrusionPlus([], Vec3())._pop(x)
_reflection_pack[ExtrusionPlus] = _prefix(
    'class python::BPPythonGeometryVolumeExtrusionPlus'.encode(encoding='GBK'))
_reflection_unpack['class python::BPPythonGeometryVolumeExtrusionPlus'] = ExtrusionPlus
