# lib test
import FanucToOPC as F
url='opc.tcp://192.168.209.180:4880/FANUC/NanoUaServer'
node='ns=1;i=301'
client,connected = F.connect(url)
b=0
for i in range(100):
    while True:
        try:
            #print (i,', ',F.get_reg_state(1,node,client))
            #F.update_reg_state(1,node,0,client,'')    
            Bool = F.get_reg_state(list(range(1,30)),node,client)
            for x in range(len(Bool)):
                print (x+1,Bool[x])
            #F.update_reg_state(1,node,4,client,'')  
            print (b,' ',i)
        except TimeoutError:
            b+=1
            continue
        break
