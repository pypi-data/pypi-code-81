import time

f = open("C:\\Users\\z17288\\AppData\\Roaming\\BCompare\\BCompare.ini", "r+")
f_content = f.readlines()
f.seek(0, 0)
f.truncate()
t = str(int(time.time()))
f.write(f_content[0])
f.write(f_content[1][:12] + t + "\n")
f.write(f_content[2][:12] + t + "\n")
f.close()
