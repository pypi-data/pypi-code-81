
#安装例子
def task1(): 
    from lmfinstall.fastdfs.v1.core import fdfs 

    pin=[
        ["root@192.168.4.206:22","rootBSTdb4@zhulong.com.cn","mdw","tracker:/data/fdfs/tracker:22122"] ,
        ["root@192.168.4.203:22","rootBSTdb1@zhulong.com.cn","sdw2","storage:group1:/data/fdfs/storage/base:/data/fdfs/storage:23000"] ,
        ["root@192.168.4.205:22","rootBSTdb2@zhulong.com.cn","standby","storage:group1:/data/fdfs/storage/base:/data/fdfs/storage:23000"]  ,
        ["root@192.168.4.204:22","rootBSTdb3@zhulong.com.cn","sdw3","storage:group2:/data/fdfs/storage/base:/data/fdfs/storage:23000"]  ,
        ["root@192.168.4.202:22","rootBSTdb5@zhulong.com.cn","sdw1","storage:group2:/data/fdfs/storage/base:/data/fdfs/storage:23000"]  
        ]


    m=fdfs(pin=pin)
    m.from_zero()


if __name__=="__main__":
    task1()