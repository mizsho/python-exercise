# %%
from concurrent import futures
import numpy as np
import time

# %%
def sleepfunc(n):
    time.sleep(n)
    print('wakeup', n)
    return n

# %%
# submitすると実行開始され, as_completedで終了まで待機？
# この例では待機は行われていない様子.
with futures.ThreadPoolExecutor(max_workers=4) as executor:
    for i in range(2):
        list_future = []
        for n in [3, 5]:
            future = executor.submit(sleepfunc, n)
            list_future.append(future)
        _ = futures.as_completed(fs=list_future)

# %%
# submitを繰り返えすよりmapを使ったほうが楽.
# 待機が行われない問題は解消されない.
with futures.ThreadPoolExecutor(max_workers=2) as thread:
    for i in range(2):
        thread.map(sleepfunc, (3, 6))

# %%
# waitを使うことで待機させることに成功.
with futures.ThreadPoolExecutor(max_workers=2) as executor:
    for i in range(2):
        list_future = []
        for n in [3, 5]:
            future = executor.submit(sleepfunc, n)
            list_future.append(future)
        (done, notdone) = futures.wait(list_future)
        for future in list_future:
            print("result", future.result())

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
pow_arr = 7
pow_partial_arr = pow_arr - 2
arr = np.random.random((10**pow_arr,2))

# %%
# 普通にやると、1.42PiBのメモリが必要となって実行できない
result = calc_dist_max(arr)

# %%
# 並列化無しで、100点ごとに距離の最大値を計算
# 実行時間：25.3s
for i in range(10**pow_partial_arr):
    result = calc_dist_max(arr[100*i:100*(i+1)])
    if i<10: print(result)

# %%
# 並列化ありで、100点ごとに距離の最大値を計算
# 実行時間：23.4s (なぜかmax_workers=2が一番早い)
# 出力を順番に取り出せていることを確認.
with futures.ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(10**(pow_partial_arr-1)):
        list_future = []
        for j in range(10):
            future = executor.submit(
                calc_dist_max, 
                arr[1000*i+100*j:1000*i+100*(j+1)]
                )
            list_future.append(future)
        (done, notdone) = futures.wait(list_future)
        if i==0:
            for future in list_future:
                print("result", future.result())

# %%
# ProcessPoolExecutorバージョン
# 実行時間：29.9s (遅くなった)
with futures.ProcessPoolExecutor(max_workers=2) as executor:
    for i in range(10**(pow_partial_arr-1)):
        list_future = []
        for j in range(10):
            future = executor.submit(
                calc_dist_max, 
                arr[1000*i+100*j:1000*i+100*(j+1)]
                )
            list_future.append(future)
        (done, notdone) = futures.wait(list_future)
        if i==0:
            for future in list_future:
                print("result", future.result())

# %%
# arrをグローバル変数にしたら、スレッド間でうまくメモリを共有できないのか実験

# %%
def calc_dist_max_idx(i1, i2):
    # arr: (x,y)座標の列=>グローバル変数とする。
    # i1, i2: arrのスライスインデックス
    # 各点の組み合わせで距離を計算し、距離が最大のインデックスを返す。
    dist = np.expand_dims(arr[i1:i2], axis=1) - np.expand_dims(arr[i1:i2], axis=0)
    dist = np.sqrt(np.sum(dist**2, axis=2))
    idx_dist_max = np.unravel_index(np.argmax(dist), dist.shape)
    return idx_dist_max

# %%
# 並列化無しで、100点ごとに距離の最大値を計算
# 実行時間：25.6s
for i in range(10**pow_partial_arr):
    result = calc_dist_max_idx(100*i, 100*(i+1))
    if i<10: print(result)

# %%
# 並列化ありで、100点ごとに距離の最大値を計算
# 実行時間：22.8s (なぜかmax_workers=2が一番早い)
# 出力を順番に取り出せていることを確認.
with futures.ThreadPoolExecutor(max_workers=4) as executor:
    for i in range(10**(pow_partial_arr-1)):
        list_future = []
        for j in range(10):
            future = executor.submit(
                calc_dist_max_idx, 
                1000*i+100*j,
                1000*i+100*(j+1)
                )
            list_future.append(future)
        (done, notdone) = futures.wait(list_future)
        if i==0:
            for future in list_future:
                print("result", future.result())
