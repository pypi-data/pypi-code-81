# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
try:
    from ..py_crawl.httpU import HttpU
except ImportError as e:
    print(e)
try:
    from .proxyCrawlerU import ProxyCrawlerU
except ImportError as e:
    print(e)
try:
    from ..py_mix.ctrlCU import CtrlCU
except ImportError as e:
    print(e)
try:
    from ..py_mix.asyncU import AsyncU
except ImportError as e:
    print(e)
try:
    from ..py_file.fileU import FileU
except ImportError as e:
    print(e)
try:
    from ..py_db.redisDBU import RedisDBU
except ImportError as e:
    print(e)
try:
    from ..py_db.mongoDBU import MongoDBU
except ImportError as e:
    print(e)
import random
import time
CHECK_BAIDU = "https://www.baidu.com"
DBName = "proxy"
CHECKED_TBNAME = "checked"
HEADER_SP = "|~H~|"

class ProxyU(PyApiB):
    """
    代理相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self):
        self.redis = None
        try:
            self.redis = RedisDBU()
        except Exception as e:
            pass
        self.mongoDB = None
        try:
            self.mongoDB = MongoDBU()
        except Exception as e:
            pass
        self.redisPreKey = "proxyU"
        self.ctrlCU = None
        
    def setRedisPreKey(self, redisPreKey):
        self.redisPreKey = redisPreKey
        
    def addProxyCrawlers(self, crawlers):
        from ..py_mix.moduleU import ModuleU
        cs = ModuleU().importClsByPcls(crawlers,ProxyCrawlerU)
        for c in cs:
            crawlerName = c
            if "." in c:
                crawlerName = c.split(".")[-1]
            self.addProxyCrawler(crawlerName, cs[c])
    
    def addProxyCrawler(self,crawlerName:str, crawler:ProxyCrawlerU):
        print(f"addProxyCrawler {crawlerName}:{crawler}")
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        proxy_crawlers[crawlerName] = crawler
        setattr(self,'proxy_crawlers',proxy_crawlers)
        
    
    def produceIpSign(self,ex=600):
        """ 生成一个ip标记，如果传入ipSign一样，会尽量返回同一个代理，ex秒后过期 """
        return self.redis.randomkey()+str(ex).zfill(5)
    
    def getExByIpsign(self, ipSign):
        return int(ipSign[-5:])
    
    def getProxyMeta(self,ipSign=None, isForNet=True):
        """ 获取一个代理 """
        ipSignKey = None if not ipSign else f"{self.redisPreKey}:ipSign:{ipSign}"
        key = f"{self.redisPreKey}:checked"
        if ipSignKey:
            cacheMeta = self.redis.get(ipSignKey)
            if cacheMeta:
                return cacheMeta, None
        _type = self.redis.type(key)
        metas = []
        if _type == "list":
            ll = self.redis.len(key)
            if ll > 0:
                ii = random.randint(0,ll-1)
                metas = self.redis.lrange(key,ii,ii+1)
        else:
            metas = self.redis.srandmember(key)
        if metas and len(metas)>0:
            meta = metas[0]
            header = None
            if isForNet and HEADER_SP in meta:
                meta,header = meta.split(HEADER_SP)
            if isForNet and "|" in meta:
                proxy = self.metaToProxy(meta)
                meta, header = self.proxyToMeta(proxy, isForNet)
            if ipSignKey:
                self.redis.set(ipSignKey,meta,ex=self.getExByIpsign(ipSign))
            return meta, self.headerTodict(header)
        return None,None
    
    def proxyToMeta(self, proxy, ipSign=None, isForNet=True):
        """ dict的代理转meta格式 """
        if proxy.get("host") == "proxyU":
            return self.getProxyMeta(ipSign, isForNet=isForNet)
        if proxy.get("user") and proxy.get("host") and proxy.get("port"):
            meta = f"http://{proxy.get('user')}:{proxy.get('pswd')}@{proxy.get('host')}:{proxy.get('port')}"
        elif proxy.get("host") and proxy.get("port"):
            meta = f"http://{proxy.get('host')}:{proxy.get('port')}"
        if not isForNet:
            perSec = proxy.get("perSec")
            sourceName = proxy.get("sourceName")
            header = proxy.get("header")
            if perSec:
                meta = f"{meta}|{perSec}"
            if sourceName:
                if not perSec:
                    meta = f"{meta}||{sourceName}"
                else:
                    meta = f"{meta}|{sourceName}"
            if header:
                meta = f"{meta}{HEADER_SP}{header}"
        return meta, self.headerTodict(proxy.get("header"))
    
    def headerTodict(self, headerStr):
        if not headerStr:
            return None
        header = {}
        headersStr = []
        if ";" in headerStr:
            headersStr = headerStr.split(";")
        else:
            headersStr = [headerStr]
        for h in headersStr:
            if ":" in h:
                k,v = h.split(":")
                if v:
                    header[k] = v
        return header
    
    def metaToProxy(self, meta):
        """ meta格式转dict代理 """
        sourceName = None
        perSec = None
        header = None
        if HEADER_SP in meta:
            meta, header = meta.split(HEADER_SP)
        if "|" in meta:
            metas = meta.split("|")
            if len(metas) >= 2:
                meta = metas[0]
                perSec = metas[1]
            if len(metas) >= 3:
                sourceName = metas[2]
        if "//" in meta:
            pInfo = meta.split("//")[1]
            user,pswd = "",""
            if "@" in pInfo:
                up, pInfo = pInfo.split("@")
                if ":" in up:
                    user,pswd = up.split(":")
                else:
                    user = up
            if ":" in pInfo:
                host, port = pInfo.split(":")
                res = {"host":host,"port":port,"user":user,"pswd":pswd}
                if sourceName:
                    res["sourceName"] = sourceName
                    res["perSec"] = perSec
                if header:
                    res["header"] = header
                return res
        return {}
        
    def __readLocalMetas(self, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        return self.redis.get_str_list(key)
        
    def __saveLocalMetas(self, metas, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        self.redis.set_str_list(key, metas[-maxLen:])
        
    def __pushLocalMetas(self, metas, type="source", maxLen=1000):
        key = f"{self.redisPreKey}:{type}"
        self.redis.rpush_str(key,metas,maxLen)
        
    def __isMetaSame(self, meta1, meta2):
        m1,m2 = meta1,meta2
        if isinstance(meta1,dict):
            m1 = meta1.get('meta')
        if isinstance(meta2,dict):
            m2 = meta2.get('meta')
        mp1 = self.metaToProxy(m1)
        mp2 = self.metaToProxy(m2)
        return all(list(map(lambda x: mp1.get(x)==mp2.get(x),["host","port"])))
    
    def __isInMetas(self, meta1, metas):
        return any(list(map(lambda x: self.__isMetaSame(meta1, x),metas)))
        
    def __upsertCheckedMeta(self, meta, maxLen=1000):
        """ 更新有效的代理入mongoDB,并同步一份至redis """
        key = f"{self.redisPreKey}:checked"
        if self.mongoDB.hasInit():
            self.mongoDB.upsert_one(DBName,CHECKED_TBNAME,{"meta":meta.get("meta")},meta)
        self.redis.sadd(key,meta.get("meta"))
        
    def __removeCheckedMeta(self, metaStr):
        """ 删除无效的代理mongoDB和redis """
        if self.mongoDB.hasInit():
            self.mongoDB.delete_many(DBName,CHECKED_TBNAME,{"meta":metaStr})
        self.__removeCheckedFromRedis(metaStr)
        
    def __removeCheckedFromRedis(self, *metaStrs):
        """ 从redis的checked中删除一个代理 """
        key = f"{self.redisPreKey}:checked"
        self.redis.srem(key,*metaStrs)
        
    def __filtHasChecked(self, proxys):
        key = f"{self.redisPreKey}:checked"
        _type = self.redis.type(key)
        ms = []
        if _type == "list":
            ll = self.redis.len(key)
            if ll > 0:
                ii = random.randint(0,ll-1)
                ms = self.redis.lrange(key,ii,ii+1)
        else:
            ms = self.redis.srandmember(key)
        newProxys = []
        for proxy in proxys:
            meta, header = self.proxyToMeta(proxy, isForNet=False)
            if not self.__isInMetas(meta, ms):
                newProxys.append(proxy)
        return newProxys
        
    def __popLocalMeta(self, type="source"):
        key = f"{self.redisPreKey}:{type}"
        return self.redis.lpop_str(key)
        
    def __saveToWaitCheck(self, proxys):
        # 将没有在等待队列中的元素搬到等待队列
        waitCheckMetas = self.__readLocalMetas("waitCheck")
        needPushs = []
        for proxy in proxys:
            meta = ""
            if isinstance(proxy,str):
                meta = proxy
            else:
                meta, header = self.proxyToMeta(proxy, isForNet=False)
            if not self.__isInMetas(meta, waitCheckMetas):
                needPushs.append(meta)
        if needPushs:
            print(f"tranProxys:{len(needPushs)}")
            self.__pushLocalMetas(needPushs, "waitCheck")
            
    def __popWaitCheck(self):
        return self.__popLocalMeta("waitCheck")
        
    def crawlProxyAndSave(self, crawlerName):
        """ 采集名称为crawlerName的爬虫，并保存所获得的代理 """
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        crawler = proxy_crawlers.get(crawlerName)
        if crawler and crawler.crawlerEnable:
            proxys = crawler().getProxys()
            print(f"crawlProxyAndSave:{len(proxys)}")
            proxys = self.__filtHasChecked(proxys)
            self.__saveToWaitCheck(proxys)
        
    def crawlProxysAndSave(self):
        """ 采集所有爬虫，并保存所获得的代理 """
        asyncU:AsyncU = AsyncU.produce("ProxyU")
        runKeys = asyncU.getRunningKeys()
        proxy_crawlers = getattr(self,'proxy_crawlers',{})
        for k in proxy_crawlers:
            if k not in runKeys:
                asyncU.asyncRun(target=self.crawlProxyAndSave,args=(k,), asyncKey=k, isProcess=False)
    
    def loopCrawl(self, crawlDuring):
        """ 循环采集所有爬虫，并保存所获得的代理 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        while not ctrlCU.isExit():
            wkey = ctrlCU.wantSleep()
            self.crawlProxysAndSave()
            ctrlCU.toSleep(crawlDuring,wkey)
        
    def checkOneProxy(self, proxyMeta=None, timeout=60, checkUrl=CHECK_BAIDU):
        """ 检测一次代理的可用性，并保存入checked。proxyMeta如果为空，则从等待队列中pop一个代理 """
        if proxyMeta == None:
            proxyMeta = self.__popWaitCheck()
        if proxyMeta:
            proxy = self.metaToProxy(proxyMeta)
            _proxyMeta, headers = self.proxyToMeta(proxy,isForNet=True)
            res = HttpU().get(checkUrl,headers=headers,proxyMeta=_proxyMeta,timeout=timeout)
            if str(res.get('code')) == "200":
                meta = {"meta":proxyMeta,"ut":time.time()}
                print(f"check {proxyMeta} Pass!!")
                self.__upsertCheckedMeta(meta)
            else:
                print(f"check {proxyMeta} NoPass!!")
                self.__removeCheckedMeta(proxyMeta)
            return True
        else:
            return False
                
    def loopCheckOneProxy(self, timeout=20, checkUrl=CHECK_BAIDU):
        """ 一个线程循环检测等待队列中代理的可用性，并保存入checked。 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        while not ctrlCU.isExit():
            res = False
            try:
                res = self.checkOneProxy(timeout=timeout,checkUrl=checkUrl)
            except Exception as e:
                print("checkOneProxy Failed!!!")
            if not res:
                time.sleep(5)
            else:
                time.sleep(1)
            
    def tranExpire(self, expireTime=600):
        """ 转移过期的入待查队列 """
        if self.mongoDB.hasInit():
            nowTime = time.time()
            needChecks = self.mongoDB.find(DBName,CHECKED_TBNAME,{"ut":{"$lte":(nowTime-expireTime)}})
            if needChecks:
                metas = list(map(lambda x: x.get("meta"),needChecks))
                self.__saveToWaitCheck(metas)
        else:
            needChecks = self.__getCheckedList()
            if needChecks:
                self.__saveToWaitCheck(needChecks)
            
    def __getCheckedList(self):
        key = f"{self.redisPreKey}:checked"
        checkeds = []
        try:
            _type = self.redis.type(key)
            if _type == "list":
                checkedset = self.redis.lrange(key,0,500)
            else:
                checkedset = self.redis.srandmember(key,number=500)
            checkeds = list(checkedset)
        except Exception as identifier:
            pass
        return checkeds
        
    def loopTranExpire(self,expireTime=600):
        """ 定时转移过期的入待查队列 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        while not ctrlCU.isExit():
            time.sleep(60)
            self.tranExpire(expireTime)
        
    def loopCheck(self,checkUrl=CHECK_BAIDU,checkTimeout=20,checkThreadNum=16,expireTime=600):
        """ 多线程循环检测等待队列中代理的可用性，并保存入checked。 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        asyncU:AsyncU = AsyncU.produce("ProxyU")
        asyncU.asyncRun(target=self.loopTranExpire, args=(expireTime,), asyncKey="loopTranExpire", isProcess=False)
        for c in range(checkThreadNum):
            asyncU.asyncRun(target=self.loopCheckOneProxy,args=(checkTimeout,checkUrl,), asyncKey=f"loopChechProxys_{c}", isProcess=False)
        
    def loopCrawlAndCheck(self,crawlDuring=20,checkUrl=CHECK_BAIDU,checkTimeout=20,checkThreadNum=16,expireTime=600):
        """ 总入口，启动所有采集和检测进程 """
        ctrlCU:CtrlCU = CtrlCU.produce("proxyU")
        ctrlCU.on()
        self.loopCheck(checkUrl=checkUrl, checkTimeout=checkTimeout,checkThreadNum=checkThreadNum,expireTime=expireTime)
        self.loopCrawl(crawlDuring)
        
    def startServer(self, port=8080):
        """ 开始总代理服务
        pip install pyopenssl
        pip install tornado
        pip install pycurl
        """
        from ..py_server.serverU import ServerU
        # from .proxyHandler import ProxyHandler
        # ServerU().http(port).addHandler(ProxyHandler).start()
        