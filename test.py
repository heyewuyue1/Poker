import signal
import time
 
def handler(signum, frame):
    print("收到了SIGALRM信号")
