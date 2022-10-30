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

# %%
def calc_dist_max(arr):
    # arr: (x,y)座標の列
    # 各点の組み合わせで距離を計算し、距離が最大のインデックスを返す。
    dist = np.expand_dims(arr, axis=1) - np.expand_dims(arr, axis=0)
    dist = np.sqrt(np.sum(dist**2, axis=2))
    idx_dist_max = np.unravel_index(np.argmax(dist), dist.shape)
    return idx_dist_max

# %%
# 100万点を用意
pow_arr = 6
pow_partial_arr = pow_arr - 2
arr = np.random.random((10**pow_arr,2))

# %%
# 並列化無しで、100点ごとに距離の最大値を計算
# 実行時間：2.5s
for i in range(10**pow_partial_arr):
    _ = calc_dist_max(arr[100*i:100*(i+1)])

# %%
# 並列化ありで、100点ごとに距離の最大値を計算
# 実行時間：24.8s（ちょうど10倍くらい）
for i in range(10**(pow_partial_arr-1)):
    list_process = []
    for j in range(10):
        list_process.append(
            Process(target=calc_dist_max, args=(arr[1000*i+100*j:1000*i+100*(j+1)],))
        )

    for p in list_process:
        p.start()

    for p in list_process:
        p.join()

# %%
# processのオーバーヘッドを確認
# 実行時間：42.7s
for i in range(10**pow_partial_arr):
    myprocess = Process(target=calc_dist_max, args=(arr[100*i:100*(i+1)],))
    myprocess.start()
    myprocess.join()

# %%
arr = None