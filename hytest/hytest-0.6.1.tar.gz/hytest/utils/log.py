_e=' case_st_lable'
_d='green'
_c='case_abort_list'
_b='case_fail_list'
_a='case_pass_list'
_Z='tag'
_Y=' fail'
_X='folder_header'
_W='executetime'
_V='folder_body'
_U='%Y%m%d_%H%M%S'
_T='用例'
_S='log'
_R='info error-info'
_Q='%Y-%m-%d %H:%M:%S'
_P='utf8'
_O='case_pass'
_N='case_count'
_M='label'
_L='suite'
_K='case_teardown_fail'
_J='suite_teardown_fail'
_I='case_setup_fail'
_H='suite_setup_fail'
_G='case_abort'
_F='case_fail'
_E='class'
_D='\n'
_C='Traceback:\n'
_B='bright_red'
_A=None
import logging,os,time
from logging.handlers import RotatingFileHandler
from rich.console import Console
from rich.theme import Theme
from hytest.product import version
from datetime import datetime
from hytest.common import GSTORE
os.makedirs(_S,exist_ok=True)
logger=logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
logFile=os.path.join(_S,'testresult.log')
handler=RotatingFileHandler(logFile,maxBytes=1024*1024*30,backupCount=2,encoding=_P)
handler.setLevel(logging.DEBUG)
formatter=logging.Formatter(fmt='%(message)s')
handler.setFormatter(formatter)
handler.doRollover()
logger.addHandler(handler)
console=Console(theme=Theme(inherit=False))
print=console.print
class LogLevel:level=0
class Stats:
	def testStart(self,_title='Test Report'):self.result={_N:0,_O:0,_F:0,_G:0,_H:0,_I:0,_J:0,_K:0,_a:[],_b:[],_c:[]};self.start_time=time.time()
	def testEnd(self):
		A='---ret---';self.end_time=time.time();self.test_duration=self.end_time-self.start_time
		if self.result[_F]or self.result[_G]or self.result[_H]or self.result[_I]or self.result[_J]or self.result[_K]:GSTORE[A]=1
		else:GSTORE[A]=0
	def enter_case(self,caseId,name,case_className):self.result[_N]+=1
	def case_pass(self,caseId,name):self.result[_O]+=1;self.result[_a].append(caseId)
	def case_fail(self,caseId,name,e,stacktrace):self.result[_F]+=1;self.result[_b].append(caseId)
	def case_abort(self,caseId,name,e,stacktrace):self.result[_G]+=1;self.result[_c].append(caseId)
	def setup_fail(self,name,utype,e,stacktrace):
		if utype==_L:self.result[_H]+=1
		else:self.result[_I]+=1
	def teardown_fail(self,name,utype,e,stacktrace):
		if utype==_L:self.result[_J]+=1
		else:self.result[_K]+=1
stats=Stats()
class ConsoleLogger:
	def testEnd(self):A='white';ret=stats.result;print(f"\n\n  ========= 测试耗时 : {stats.test_duration:.3f} 秒 =========\n");print(f"\n  用例数量 : {ret[_N]}");print(f"\n  通过 : {ret[_O]}",style=_d);num=ret[_F];style=A if num==0 else _B;print(f"\n  失败 : {num}",style=style);num=ret[_G];style=A if num==0 else _B;print(f"\n  异常 : {num}",style=style);num=ret[_H];style=A if num==0 else _B;print(f"\n  套件初始化失败 : {num}",style=style);num=ret[_J];style=A if num==0 else _B;print(f"\n  套件清除  失败 : {num}",style=style);num=ret[_I];style=A if num==0 else _B;print(f"\n  用例初始化失败 : {num}",style=style);num=ret[_K];style=A if num==0 else _B;print(f"\n  用例清除  失败 : {num}",style=style)
	def enter_suite(self,name,suitetype):
		if suitetype=='file':print(f"\n\n>>> {name}",style='bold bright_black')
	def enter_case(self,caseId,name,case_className):print(f"\n* {name}",style='bright_white')
	def case_steps(self,name):...
	def case_pass(self,caseId,name):print('                          PASS',style=_d)
	def case_fail(self,caseId,name,e,stacktrace):print(f"                          FAIL\n{e}",style=_B)
	def case_abort(self,caseId,name,e,stacktrace):print(f"                          ABORT\n{e}",style='magenta')
	def case_check_point(self,msg):...
	def setup(self,name,utype):...
	def teardown(self,name,utype):...
	def setup_fail(self,name,utype,e,stacktrace):utype='套件'if utype==_L else _T;print(f"\n{utype} 初始化失败 | {name} | {e}",style=_B)
	def teardown_fail(self,name,utype,e,stacktrace):utype='套件'if utype==_L else _T;print(f"\n{utype} 清除失败 | {name} | {e}",style=_B)
	def debug(self,msg):
		if LogLevel.level>0:print(f"{msg}")
	def criticalInfo(self,msg):print(f"{msg}",style=_B)
class TextLogger:
	def testStart(self,_title=''):startTime=time.strftime(_U,time.localtime(stats.start_time));logger.info(f"\n\n  ========= 测试开始 : {startTime} =========\n")
	def testEnd(self):endTime=time.strftime(_U,time.localtime(stats.end_time));logger.info(f"\n\n  ========= 测试结束 : {endTime} =========\n");logger.info(f"\n  耗时    : {stats.end_time-stats.start_time:.3f} 秒\n");ret=stats.result;logger.info(f"\n  用例数量 : {ret[_N]}");logger.info(f"\n  通过 : {ret[_O]}");logger.info(f"\n  失败 : {ret[_F]}");logger.info(f"\n  异常 : {ret[_G]}");logger.info(f"\n  套件初始化失败 : {ret[_H]}");logger.info(f"\n  套件清除  失败 : {ret[_J]}");logger.info(f"\n  用例初始化失败 : {ret[_I]}");logger.info(f"\n  用例清除  失败 : {ret[_K]}")
	def enter_suite(self,name,suitetype):logger.info(f"\n\n>>> {name}")
	def enter_case(self,caseId,name,case_className):curTime=datetime.now().strftime(_Q);logger.info(f"\n* {name}  -  {curTime}")
	def case_steps(self,name):logger.info(f"\n  [ case execution steps ]")
	def case_pass(self,caseId,name):logger.info('  PASS ')
	def case_fail(self,caseId,name,e,stacktrace):stacktrace=_C+stacktrace.split(_D,3)[3];logger.info(f"  FAIL   {e} \n{stacktrace}")
	def case_abort(self,caseId,name,e,stacktrace):stacktrace=_C+stacktrace.split(_D,3)[3];logger.info(f"  ABORT   {e} \n{stacktrace}")
	def case_check_point(self,msg):logger.info(f"\n-- check {msg}")
	def setup(self,name,utype):logger.info(f"\n[ {utype} setup ] {name}")
	def teardown(self,name,utype):logger.info(f"\n[ {utype} teardown ] {name}")
	def setup_fail(self,name,utype,e,stacktrace):stacktrace=_C+stacktrace.split(_D,3)[3];logger.info(f"{utype} setup fail | {e} \n{stacktrace}")
	def teardown_fail(self,name,utype,e,stacktrace):stacktrace=_C+stacktrace.split(_D,3)[3];logger.info(f"{utype} teardown fail | {e} \n{stacktrace}")
	def info(self,msg):logger.info(msg)
	def debug(self,msg):
		if LogLevel.level>0:logger.debug(msg)
	def step(self,stepNo,desc):logger.info(f"\n-- 第 {stepNo} 步 -- {desc} \n")
	def checkpoint_pass(self,desc):logger.info(f"\n** 检查点 **  {desc} ---->  通过\n")
	def checkpoint_fail(self,desc):logger.info(f"\n** 检查点 **  {desc} ---->  !! 不通过!!\n")
	def criticalInfo(self,msg):logger.info(f"!!! {msg} !!!")
	def log_img(self,imgPath,width=_A):logger.info(f"图 {imgPath}")
from dominate.tags import *
from dominate.util import raw
from dominate import document
class HtmlLogger:
	def __init__(self):self.curEle=_A
	def testStart(self,_title=''):
		A='menu-item'
		with open(os.path.join(os.path.dirname(__file__),'report.css'),encoding=_P)as f:_css_style=f.read()
		with open(os.path.join(os.path.dirname(__file__),'report.js'),encoding=_P)as f:_js=f.read()
		self.doc=document(title=f"测试报告");self.doc.head.add(meta(charset='UTF-8'),style(raw(_css_style)),script(raw(_js),type='text/javascript'));self.main=self.doc.body.add(div(_class='main_section'));self.main.add(h1(f"测试报告 - hytest v{version}",style='font-family: auto'));_,self.stats=self.main.add(h3(f"统计结果"),table(_class='result_stats'));_,self.logDiv=self.main.add(div(h3('执行日志',style='display:inline'),style='margin-top:2em'),div(_class='exec_log'));self.ev=div(div('∧',_class=A,onclick='previous_error()',title='上一个错误'),div('∨',_class=A,onclick='next_error()',title='下一个错误'),_class='error_jumper');self.main.add(div(div('页首',_class=A,onclick='document.querySelector("body").scrollIntoView()'),div('教程',_class=A,onclick='window.open("http://www.byhy.net/tut/auto/hytest/01", "_blank"); '),div('精简',_class=A,id='display_mode',onclick='toggle_folder_all_cases()'),self.ev,id='float_menu'));self.curEle=self.main;self.curSuiteEle=_A;self.curCaseEle=_A;self.curCaseLableEle=_A;self.curSetupEle=_A;self.curTeardownEle=_A;self.suitepath2element={}
	def testEnd(self):
		B='%Y%m%d %H:%M:%S';A='color:red';execStartTime=time.strftime(B,time.localtime(stats.start_time));execEndTime=time.strftime(B,time.localtime(stats.end_time));ret=stats.result;errorNum=0;trs=[];trs.append(tr(td('开始时间'),td(f"{execStartTime}")));trs.append(tr(td('结束时间'),td(f"{execEndTime}")));trs.append(tr(td('耗时'),td(f"{stats.test_duration:.3f} 秒")));trs.append(tr(td('用例数量'),td(f"{ret[_N]}")));trs.append(tr(td('通过'),td(f"{ret[_O]}")));num=ret[_F];style=''if num==0 else A;trs.append(tr(td('失败'),td(f"{num}",style=style)));errorNum+=num;num=ret[_G];style=''if num==0 else A;trs.append(tr(td('异常'),td(f"{num}",style=style)));errorNum+=num;num=ret[_H];style=''if num==0 else A;trs.append(tr(td('套件初始化失败'),td(f"{num}",style=style)));errorNum+=num;num=ret[_J];style=''if num==0 else A;trs.append(tr(td('套件清除失败'),td(f"{num}",style=style)));errorNum+=num;num=ret[_I];style=''if num==0 else A;trs.append(tr(td('用例初始化失败'),td(f"{num}",style=style)));errorNum+=num;num=ret[_K];style=''if num==0 else A;trs.append(tr(td('用例清除失败'),td(f"{num}",style=style)));errorNum+=num;self.ev['display']='none'if errorNum==0 else'block';self.stats.add(tbody(*trs));htmlcontent=self.doc.render();timestamp=time.strftime(_U,time.localtime(stats.start_time));reportFile=os.path.join(_S,f"log_{timestamp}.html")
		with open(reportFile,'w',encoding=_P)as f:f.write(htmlcontent)
		try:os.startfile(reportFile)
		except:
			try:os.system(f"open {reportFile}")
			except:...
	def enter_suite(self,name,suitetype):_class='suite_'+suitetype;enterInfo='进入目录'if suitetype=='dir'else'进入文件';self.curEle=self.logDiv.add(div(div(span(enterInfo,_class=_M),span(name)),_class=_class,id=f"{_class} {name}"));self.curSuiteEle=self.curEle;self.curSuiteFilePath=name;self.suitepath2element[name]=self.curEle
	def enter_case(self,caseId,name,case_className):self.curCaseLableEle=span(_T,_class='label caselabel');self.curCaseBodyEle=div(span(f"{self.curSuiteFilePath}::{case_className}",_class='case_class_path'),_class=_V);self.curCaseEle=self.curSuiteEle.add(div(div(self.curCaseLableEle,span(name,_class='casename'),span(datetime.now().strftime(_Q),_class=_W),_class=_X),self.curCaseBodyEle,_class='case',id=f"case_{caseId:08}"));self.curEle=self.curCaseBodyEle
	def case_steps(self,name):ele=div(span('测试步骤',_class=_M),_class='test_steps',id='test_steps '+name);self.curEle=self.curCaseBodyEle.add(ele)
	def case_pass(self,caseId,name):self.curCaseEle[_E]+=' pass';self.curCaseLableEle+=' PASS'
	def case_fail(self,caseId,name,e,stacktrace):self.curCaseEle[_E]+=_Y;self.curCaseLableEle+=' FAIL';stacktrace=_C+stacktrace.split(_D,3)[3];self.curEle+=div(f"{e} \n{stacktrace}",_class=_R)
	def case_abort(self,caseId,name,e,stacktrace):self.curCaseEle[_E]+=' abort';self.curCaseLableEle+=' ABORT';stacktrace=_C+stacktrace.split(_D,3)[3];self.curEle+=div(f"{e} \n{stacktrace}",_class=_R)
	def case_check_point(self,msg):0
	def setup(self,name,utype):
		_class=f"{utype}_setup setup"
		if utype==_L:stHeaderEle=div(span('套件初始化',_class=_M),span(name),span(datetime.now().strftime(_Q),_class=_W),_class=_X);stBodyEle=self.curEle=div(_class=_V);self.curSetupEle=div(stHeaderEle,stBodyEle,_class=_class,id=f"{_class} {name}");self.curSuiteEle.add(self.curSetupEle)
		else:self.curSetupEle=self.curEle=div(span('用例初始化',_class=_M),_class=_class,id=f"{_class} {name}");self.curCaseBodyEle.add(self.curSetupEle);self.curEle[_E]+=_e
	def teardown(self,name,utype):
		_class=f"{utype}_teardown teardown"
		if utype==_L:stHeaderEle=div(span('套件清除',_class=_M),span(name),span(datetime.now().strftime(_Q),_class=_W),_class=_X);stBodyEle=self.curEle=div(_class=_V);self.curTeardownEle=div(stHeaderEle,stBodyEle,_class=_class,id=f"{_class} {name}");self.curSuiteEle.add(self.curTeardownEle)
		else:self.curTeardownEle=self.curEle=div(span('用例清除',_class=_M),_class=_class,id=f"{_class} {name}");self.curCaseBodyEle.add(self.curTeardownEle);self.curEle[_E]+=_e
	def setup_fail(self,name,utype,e,stacktrace):self.curSetupEle[_E]+=_Y;stacktrace=_C+stacktrace.split(_D,3)[3];self.curEle+=div(f"{utype} setup fail | {e} \n{stacktrace}",_class=_R)
	def teardown_fail(self,name,utype,e,stacktrace):self.curTeardownEle[_E]+=_Y;stacktrace=_C+stacktrace.split(_D,3)[3];self.curEle+=div(f"{utype} teardown fail | {e} \n{stacktrace}",_class=_R)
	def info(self,msg):
		if self.curEle is _A:return
		self.curEle+=div(msg,_class='info')
	def step(self,stepNo,desc):
		if self.curEle is _A:return
		self.curEle+=div(span(f"第 {stepNo} 步",_class=_Z),span(desc),_class='case_step')
	def checkpoint_pass(self,desc):
		if self.curEle is _A:return
		self.curEle+=div(span(f"检查点 PASS",_class=_Z),span(desc),_class='checkpoint_pass')
	def checkpoint_fail(self,desc):
		if self.curEle is _A:return
		self.curEle+=div(span(f"检查点 FAIL",_class=_Z),span(desc),_class='checkpoint_fail')
	def log_img(self,imgPath,width=_A):
		if self.curEle is _A:return
		self.curEle+=div(img(src=imgPath,width='aa'if width is _A else width,_class='screenshot'))
from .signal import signal
signal.register([stats,ConsoleLogger(),TextLogger(),HtmlLogger()])