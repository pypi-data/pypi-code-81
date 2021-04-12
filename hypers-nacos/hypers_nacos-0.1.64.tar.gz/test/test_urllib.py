from urllib.request import Request, urlopen

req = Request("https://www.baidu.com:443/")
ret = urlopen(req)

req = Request("http://127.0.0.1:8848/nacos/", headers={'Host': '127.0.0.1'})
ret = urlopen(req)
print(ret.read())

req = Request("https://nacos.hypers.cc:443/nacos/v1/cs/configs?username=admin&password=criusadmin", headers={'Host': 'nacos.hypers.cc'})
import ipdb;ipdb.set_trace()
ret = urlopen(req)
# urlopen 在不指定 headers 会自动添加 headers, headers 默认会添加 Host, 
# 添加的 Host 是由 域名 和 端口 生成的，如：
# url = "https://nacos.hypers.cc:443/nacos/v1/cs/configs?username=admin&password=criusadmin"
# 自动添加的 headers: {'Host': 'nacos.hypers.cc:443'}
# url = "http://127.0.0.1:8848/nacos/"
# 自动添加的 headers: {'Host': '127.0.0.1:8848'}
# 有些服务器 Host 头指定不正确会报 URL NOT FOUND（404）的错误
# nacos.hypers.cc 服务器就必须指定 headers 为 {'Host': 'nacos.hypers.cc'} 才能正确访问
