import subprocess
import time
import sys

DETACHED_PROCESS = 0x00000008


# kill existing process
subprocess.Popen("taskkill /F /IM main_sms.exe")
subprocess.Popen("taskkill /F /IM sms_ui.exe")

time.sleep(2)
pid = subprocess.Popen("main_sms.exe",
                       creationflags=DETACHED_PROCESS).pid

time.sleep(2)
#pid = subprocess.Popen([sys.executable, "sms_ui.exe"],
#                       creationflags=DETACHED_PROCESS).pid
pid = subprocess.Popen("sms_ui.exe",shell=True,
                       creationflags=DETACHED_PROCESS).pid

quit()
