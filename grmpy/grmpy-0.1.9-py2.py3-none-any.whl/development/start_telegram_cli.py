import subprocess

os.chdir("../..")
os.chdir("snap/telegram")
subprocess.check_call(["telegram-cli"])

