import importlib,os,sys,time,json

class BaseTest:
    _testmode = False
    
    _modules_ = []
    
    _cases_ = []
    msg = ""
    mastpass = []
    pass

def assertImport(module):
    try:
        m = importlib.import_module(module)
        return m
    except Exception as err:
        #print(r"引入模块[{}]异常！".format(module))
        raise AssertionError(r"import [{}] failed！because:{}".format(module,str(err)))
    pass


def assertEqual(arg1,arg2,msg = None):
    assertmsg = r"{} is not equal to {}".format(arg1,arg2)
    if msg:
        assertmsg += " ({})".format(msg)
    assert arg1 == arg2,assertmsg

def assertTrue(expr,msg = None):
    if not msg:
        msg = "assert"
    assertmsg = r"{} is not a true expression".format(msg)
    
    assert expr,assertmsg

def setup(module,reload=True):
    #if modulepath ins_MethodTest._modules_
    abspath = os.path.abspath(module)
    """
    if abspath in ins_MethodTest._modules_:
        if reload:
            importlib.reload(module)
            print(r"reload [{}] successed!".format(module))
        return
    """
    try:
        m = assertImport(module)
        print(r"import [{}] successed！".format(module))
        ins_MethodTest._modules_.append(abspath)
        return m
    except AssertionError as err:
        print(err)
    
    #print(ins_MethodTest._modules_)
    pass

def case(msg = "have not set message yet",mastpass=[]):
    
    ins_MethodTest.msg = msg
    ins_MethodTest.mastpass = mastpass
    return testfuncwrapper
    
def testfuncwrapper(func):
    if ins_MethodTest._testmode:
        ins_MethodTest._cases_.append({'file':func.__globals__['__file__'],'name':func.__name__,'func':func,'msg':ins_MethodTest.msg,"mastpass":ins_MethodTest.mastpass})
    
    return func

def test(resultpath=r"./"):
    rtn = {"spend":0.0,"cases":{}}
    gs = time.time()
    for testcase in ins_MethodTest._cases_:
        file = testcase["file"]
        name = testcase["name"]
        func = testcase["func"]
        print('-'*20)
        if not file in rtn["cases"]:
            rtn["cases"][file] = {}
        rtn["cases"][file][name] = {}
        
        report = rtn["cases"][file][name]
        cs = time.time()
        
        try:
            func()
            print("{} test passed".format(name))
            report["result"] = "passed"
            
        except AssertionError as err:
            
            print("[line:{}] {} test failed! ({})".format(err.__traceback__.tb_next.tb_lineno,name,str(err)))
            report["result"] = "failed"
            report["message"] = "[line:{}]:{}".format(err.__traceback__.tb_next.tb_lineno,str(err))
            
        ce = time.time()
        report["spend"] = round(ce-cs,3)
    ge = time.time()
    rtn["spend"] = round(ge-gs,3)
    
    try:
        resultfile = os.path.join(resultpath,"rst.txt")
        with open(resultfile,'w') as f:
            json.dump(rtn,f,indent = 4)
    except Exception as err:
        print("Save test result failed;")
        print(err)
    pass


class MethodTest(BaseTest):
    
    pass


    
ins_MethodTest = MethodTest()