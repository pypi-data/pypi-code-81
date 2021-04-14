import os
class WIFI(object):
    def __init__(self,ssid='null',pwd='null'):
        self.set_conf(ssid, pwd)
        self.init()
    def command(self,cmd):
        process = os.popen(cmd) # return file
        out = process.read()
        process.close()
        return out
    def is_exist(self):
        if self.command('cat /proc/net/dev|grep "wlan0"') == '':
            return False
        return True
    def enable(self):
        if self.command('ifconfig|grep "wlan0"') == '':
            self.command("ifconfig wlan0 up")
            return True
            
    def disable(self):
        if self.command('ifconfig|grep "wlan0"') != '':
            self.command("ifconfig wlan0 down")   
            return True
    def status(self):
        return self.command('ifconfig|grep "wlan0"') != ''
    def init(self):
        if self.is_exist() == False:
            self.command("insmod /ko/esp8089.ko")   
            timeout = 10
            while self.is_exist() == False and timeout > 0:
                time.sleep(0.5)
                timeout -= 1
            if self.is_exist() == False:
                print("load wifi driver fail.")
                return False
    def getip(self):
        return self.command("ifconfig wlan0|grep \"inet\"|awk \'{print $2}\'").replace('\n', '')
    def set_conf(self,ssid, pwd):
        conf = \
        "\
        ctrl_interface=/var/run/wpa_supplicant\n\
        \n\
        network={\n\
                ssid=\"%s\"\n\
                psk=\"%s\"\n\
                proto=WPA2\n\
        }\
        " %(ssid, pwd)  
        f = open("/etc/wifi.conf","w+")
        f.write(conf)
        f.close()
        return conf
    def connect(self):
        if self.getip() != '':
            return 
        if self.command("pidof wpa_supplicant") != '':
            self.command("pidof wpa_supplicant|xargs kill -9")
        if self.command("pidof udhcpc") != '':
            self.command("pidof udhcpc|xargs kill -9")
        self.disable()
        if self.status() == False:
            self.enable()
        self.command("wpa_supplicant -B -Dwext -iwlan0 -c /etc/wifi.conf &")
        self.command("udhcpc -iwlan0 &")
        timeout = 10
        while self.getip() == '' and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if self.getip() == '':
            return False