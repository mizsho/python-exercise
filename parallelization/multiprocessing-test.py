# %%
from multiprocessing import Process, Queue
import numpy as np
import time

# %%
def sleepfunc(n):
    time.sleep(n)
    print('wakeup', n)

# %%
for i in range(2):
    # プロセスを定義
    process1 = Process(target=sleepfunc, args=(1,))
    process2 = Process(target=sleepfunc, args=(3,))

    # プロセスを開始
    process1.start()
    process2.start()

    # プロセスが終了するまで待機
    process1.join()
    process2.join()
