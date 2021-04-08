'''
Created on 2020-11-22

@author: zhanyifei
'''
import holowan.HoloWAN
from holowan.HoloWAN import HoloWAN
import re
import os
import configparser
import testcase
import time
import datetime



#Common configuration
# holowan_ip = "10.85.60.66"
holowan_ip = "192.168.1.223"
holowan_port = "8080"
engineID = 1
holowan = HoloWAN()
#path configuration
filepath = os.path.join(os.getcwd(), 'config.txt')
cp = configparser.ConfigParser(converters={'toint':int})
cp.read(filepath)
path_num = cp.gettoint('config', 'path_num')
pathName = 'PATH'
testip = cp.get('config', 'testip')
audioTime = cp.gettoint('config', 'audioTime')
videoTime = cp.gettoint('config', 'videoTime')



# 0 = close;1 = open
enableReordering = cp.gettoint('config', 'enableReordering')

#Test Equipment ip config
TOS = "any"
sourceMask = 32
destinationMask =32

#simple config
Background_burst = 64



def init():
    #in admin button to remove password 
    password = 4123456789
    new_password = 4123456789
    response = holowan.hold_engine(holowan_ip=holowan_ip, holowan_port=holowan_port, engineID=engineID, password=password, new_password=new_password)
    print("hold_engine" + response)
    
def add_path():
    response = holowan.add_path(holowan_ip=holowan_ip, holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathName=pathName)
    print('add_path'+response)
    errCode = re.compile(r'\d+') 
    x = errCode.findall(response)
    if '0' not in x:
        #print(111)
        remove_path()
    else:
        #print(222)
        return


def remove_path():
    response = holowan.remove_path(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathName=pathName)
    print('remove_path'+response)   

def open_path():
    response = holowan.open_path(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathName=pathName)
    print('open_path'+response)
    
def set_path_direction():
    response = holowan.set_path_direction(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=3)
    print('set_path'+response)


#set BWE 
def set_path_Bandwidth_Fixed(pathDirection,bwe_rateValue):
    response = holowan.set_path_Bandwidth_Fixed(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,rateValue=bwe_rateValue,rateUnit=2)
    print("set_path_Bandwidth_Fixed" + response + "， 带宽值:" + str(bwe_rateValue))

def set_Background_Utilization(pathDirection,bwe_rate):
    response = holowan.set_Background_Utilization(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,rate=bwe_rate,burst=Background_burst)
    print("set_Background_Utilization" + response)

def close_Background_Utilization(pathDirection):
    response = holowan.close_Background_Utilization(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection)
    print(response)

def set_Queue_Limit_Drop_Tail(pathDirection,queue_DepthValue,queueDepthType):
    response = holowan.set_Queue_Limit_Drop_Tail(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,queueDepthValue=queue_DepthValue,queueDepthType=queueDepthType)
    print("set_Queue_Limit_Drop_Tail" + response)

# set delay 
def set_Delay_Constant(pathDirection,delay):
    response = holowan.set_Delay_Constant(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,delay=delay)
    print(response)

def set_Delay_Uniform(pathDirection,minimum,maximum):
    response = holowan.set_Delay_Uniform(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,minimum=minimum,maximum=maximum,enableReordering=enableReordering)
    print(response)

def set_Delay_Normal(pathDirection,mean,delay_min,stdDeviation):
    response = holowan.set_Delay_Normal(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,min=delay_min,mean=mean,stdDeviation=stdDeviation,enableReordering=enableReordering)
    print(response)

def set_Delay_Normal_AdvancedSetup(pathDirection,mean,delay_min,stdDeviation,advancedPeriod,adcancedDuration,advancedMin,advancedMax):
    response = holowan.set_Delay_Normal_AdvancedSetup(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,min=delay_min,mean=mean,stdDeviation=stdDeviation,enableReordering=enableReordering,advancedPeriod=advancedPeriod,advancedDuration=adcancedDuration,advancedMin=advancedMin,advancedMax=advancedMax)
    print(response)



#set loss
def set_Loss_Cycle(pathDirection,period,loss_burst):
    response = holowan.set_Loss_Cycle(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,period=period,burst=loss_burst)
    print(response)

def set_Loss_Random(pathDirection,rate):
    response = holowan.set_Loss_Random(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,rate=rate)
    print(response)


def set_Loss_Burst(pathDirection,probability,loss_minimum,loss_maximum):
    response = holowan.set_Loss_Burst(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,probability=probability,minimum=loss_minimum,maximum=loss_maximum)
    print(response)

def set_Loss_Dual(pathDirection,goodStateLoss,goodToBadProbability,badStateLoss,badToGoodProbability):
    response = holowan.set_Loss_Dual(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,goodStateLoss=goodStateLoss,goodToBadProbability=goodToBadProbability,badStateLoss=badStateLoss,badToGoodProbability=badToGoodProbability)
    print(response)


# set base     
def set_BER(pathDirection,bitErrorValue,bitErrorIndex):
    response = holowan.set_BER(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num,pathDirection=pathDirection,bitErrorValue=bitErrorValue,bitErrorIndex=bitErrorIndex)
    print(response)

def add_IPV4_to_Classifier(portID,sourceIP,destinationIP):
    response = holowan.add_IPV4_to_Classifier(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,portID=portID,sourceIP=sourceIP,sourceMask=sourceMask,destinationIP=destinationIP,destinationMask=destinationMask,TOS=TOS,action=path_num)
    print("add_IPV4_to_Classifier" + response)


def add_test_ip(testip):
    add_IPV4_to_Classifier(2,'any',testip)
    add_IPV4_to_Classifier(1,testip,'any')

def remove_IPV4_to_Classifier(portID,sourceIP,destinationIP):
    response = holowan.remove_IPV4_from_Classifier(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,portID=portID,sourceIP=sourceIP,sourceMask=sourceMask,destinationIP=destinationIP,destinationMask=destinationMask,TOS=TOS,action=path_num)
    print("remove_IPV4_to_Classifier" + response)


def remove_test_ip(testip):
    remove_IPV4_to_Classifier(2,'any',testip)
    remove_IPV4_to_Classifier(1,testip,'any')


def start_engine():
    response = holowan.start_engine(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID)
    print("start_engine" + response)
    
def stop_engine():
    response = holowan.stop_engine(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID)
    print("stop_engine" + response)

def save_HoloWAN_information():
    response = holowan.save_HoloWAN_information(holowan_ip=holowan_ip,holowan_port=holowan_port)
    print(response)
    
def resetPath():
    response = holowan.resetPath(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,pathID=path_num)
    print("resetPath" + response)
    
def resetClassifier():
    response1 = holowan.resetClassifier(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,portID=1)
    response2 = holowan.resetClassifier(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID,portID=2)
    print("resetClassifier" + response1)
    print("resetClassifier" + response2)

def resetEngine():
    response = holowan.resetEngine(holowan_ip=holowan_ip,holowan_port=holowan_port,engineID=engineID)
    print(response)

def autotest():
    brand = 'lark'
    flag = '_'
    name = 0
    list2 = testcase.excel_data('qos.xlsx')
    list1 = list2[0]    
    for i in range(0, list2[0]-1):
        x = 22 * i
        print(x)
        #Direction parameter
        if '1' in list2[x+1]:
            pathDirection = 1
 
        else:
            pathDirection = 2
        #bwe parameter
        if 'closed' == list2[x+2]:
            print('bwe closed')
        else:
            bwe_rateValue = list2[x+3]
            bwe_rate = list2[x+4]
            queue_DepthValue = list2[x+5]
            print(type(queue_DepthValue))
            
            if 'KB' in list2[x+6]:
                queueDepthType = 2           
            elif 'Packets' in list2[x+6]:
                queueDepthType = 1
            else:
                queueDepthType = 3
            
            set_path_Bandwidth_Fixed(pathDirection,bwe_rateValue)
            set_Background_Utilization(pathDirection,bwe_rate)
            set_Queue_Limit_Drop_Tail(pathDirection,queue_DepthValue,queueDepthType)
        
        
        #delay parameter       
        if 'Constant' == list2[x+7]:
            print('This is Constant delay')
            delay = list2[x+8]
            set_Delay_Constant(pathDirection,delay)
            # time.sleep(1)
            
        elif 'Normal' == list2[x+7]:
            print('This is Normal delay')
            mean = list2[x+8]
            delay_min = list2[x+9]
            stdDeviation = list2[x+10]
            set_Delay_Normal(pathDirection,mean,delay_min,stdDeviation)
            
        elif 'Uniform' == list2[x+7]:
            print('This is Uniform delay')
            minimum = list2[x+9]
            maximum = list2[x+10]
            set_Delay_Uniform(pathDirection,minimum,maximum)
        
        elif 'Advanced' == list2[x+7]:
            print('This is special delay')
            mean = list2[x+8]
            delay_min = list2[x+9]
            stdDeviation = list2[x+10]
            advancedPeriod = list2[x+11]
            adcancedDuration =list2[x+12]
            advancedMin = list2[x+13]
            advancedMax = list2[x+14]
            set_Delay_Normal_AdvancedSetup(pathDirection,mean,delay_min,stdDeviation,advancedPeriod,adcancedDuration,advancedMin,advancedMax)
        else:
            print('delay closed')
        
        
        #loss parameter     
        if 'closed' == list2[x+15]:
            print('loss closed')
        
        elif 'Random' == list2[x+15]:
            rate = list2[x+18]  
            set_Loss_Random(pathDirection,rate)
            
        elif 'Burst' == list2[x+15]:
            probability = list2[x+18] 
            loss_minimum = list2[x+16]
            loss_maximum = list2[x+17]
            set_Loss_Burst(pathDirection,probability,loss_minimum,loss_maximum)
            
        
        elif 'Cycle' == list2[x+15]:
            period = list2[x+16]
            loss_burst = list2[x+17]
            set_Loss_Cycle(pathDirection,period,loss_burst)
        
        else:
            goodStateLoss = list2[x+18]
            goodToBadProbability = list2[x+19]
            badStateLoss = list2[x+20]
            badToGoodProbability = list2[x+21]           
            set_Loss_Dual(pathDirection,goodStateLoss,goodToBadProbability,badStateLoss,badToGoodProbability)
        
        print(datetime.datetime.now().strftime('%H:%M:%S.%f'))
        start_engine()
        print('teststart')
        test_time = list2[x+22]
        print(test_time)
        # time.sleep(test_time)
        stop_engine()
        # time.sleep(videoTime)
        # resetPath()
        print("="*20)
        time.sleep(100)

if __name__ == '__main__':
    init()
    add_path()
    set_path_direction()
    open_path()
    resetPath()
    add_test_ip(testip)
    autotest()
    remove_test_ip(testip)
    resetClassifier()
    print('over')

