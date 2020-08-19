import webview
import os
import time
from subprocess import Popen
import psutil

# Start Django Server
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY_EXEC = BASE_DIR + "\\fin_env\\python.exe"
SERVER_EXEC = BASE_DIR + "\\cash_book_pc\\manage.py"

Logs = open(BASE_DIR + "\\logs_out.txt", "a+")
Error = open(BASE_DIR + "\\logs_err.txt", "a+")

process = Popen([PY_EXEC, SERVER_EXEC, "job_init"], universal_newlines=True)
if process.returncode is not None and  process.returncode != 0:
    print("Error occurred. Please restart application")
    input()

if process.returncode is None or process.returncode == 0:
    process = Popen([PY_EXEC, SERVER_EXEC, "runserver", "127.0.0.1:55750"], stdout=Logs, stderr=Error,
                    universal_newlines=True)

    time.sleep(5)
    window = webview.create_window("Cash Book", url="http://127.0.0.1:55750/admin", resizable=True, confirm_close=True)
    webview.start()

    Logs.close()
    Error.close()
    # Stop Django Server
    if window.closed:
        try:
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                os.popen('TASKKILL /PID {} /F'.format(child.pid))
        except:
            pass
        os.popen('TASKKILL /PID {} /F'.format(process.pid))
        print("Closed")

