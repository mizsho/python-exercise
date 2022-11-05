# %%
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

# %%
# 集合arr1とarr2の点同士ですべての組み合わせに対し距離を計算する

# %%
# まず小さい問題で試す
arr1_small = np.array([[0,0], [1,0], [1,1]])
arr2_small = np.array([[1,0], [0,1], [1,1]])
arr1_id_small = np.arange(3)
arr2_id_small = np.arange(3)

# %%
# 方法A: ブロードキャストを活用
arr_dist = np.expand_dims(arr1_small, axis=1) - np.expand_dims(arr2_small, axis=0)
arr_dist = np.sqrt(np.sum(arr_dist**2, axis=2))

# reshape(-1)はビューを返すのでメモリの節約になる
# ravelも可能な限りビューを返すが常にとは限らない
# flattenはコピーを返すので避ける
arr_dist_reshape = arr_dist.reshape((-1))

# %%
# 方法B: scipyのcdist
arr_dist = cdist(arr1_small, arr2_small)
arr_dist_reshape = arr_dist.reshape((-1))

# %%
# 方法C: 行列積でtileを表現(メモリ使用量律速になると思われる)
n1 = len(arr1_small)
n2 = len(arr2_small)
arr_dot_1 = np.ones(n2)
arr_dot_2 = np.zeros(n1*n2)
arr_dot_3 = np.hstack([arr_dot_1, arr_dot_2])
arr_dot_4 = np.tile(arr_dot_3, reps=n1)[:n1**2*n2]
arr_dot_5 = arr_dot_4.reshape((n1, n1*n2)).T

arr1_rep = arr_dot_5 @ arr1_small
arr2_rep = np.tile(arr2_small, reps=(n1, 1))
arr_dist_reshape = np.sqrt(np.sum((arr1_rep - arr2_rep)**2, axis=1))

# %%
# 出力用に成型する場合
arr_dist_msk = arr_dist_reshape < 0.25
df = pd.DataFrame(data={
    'id1': np.tile(arr1_id_small, reps=(len(arr2_small), 1)).T.reshape((-1))[arr_dist_msk],
    'id2': np.tile(arr2_id_small, reps=len(arr1_small))[arr_dist_msk],
    'dist': arr_dist_reshape[arr_dist_msk]})

# %%
# 結果確認用
df

# %%
# 大きい問題に拡張する
# ndarrayの(メモリをできるだけ使わない?)分割方法も問題となる

# テストデータ
# 集合arr1とarr2の点同士ですべての組み合わせに対し距離を計算する
pow_arr = 4
arr1 = np.random.random((10**pow_arr,2))
arr2 = np.random.random((10**pow_arr,2))
arr1_id = np.arange(len(arr1))
arr2_id = np.arange(len(arr2))

# 10**4のケース
# 方法A: 3.2s
# 方法B: 0.2s
# 方法C: 23.2s 

# 10**5のケース
# 方法A: 4m54.6s
# 方法B: 27.4s
# 方法C: ---s

method="B"

for i1 in range(10**(pow_arr - 2)):
    arr1_small = arr1[100*i1:100*(i1+1)]
    arr1_id_small = arr1_id[100*i1:100*(i1+1)]

    for i2 in range(10**(pow_arr - 2)):
        arr2_small = arr2[100*i2:100*(i2+1)]
        arr2_id_small = arr2_id[100*i2:100*(i2+1)]

        # 方法A
        if method=="A":
            arr_dist = np.expand_dims(arr1_small, axis=1) - np.expand_dims(arr2_small, axis=0)
            arr_dist = np.sqrt(np.sum(arr_dist**2, axis=2))
            arr_dist_reshape = arr_dist.reshape((-1))

        # 方法B
        elif method=="B":
            arr_dist = cdist(arr1_small, arr2_small)
            arr_dist_reshape = arr_dist.reshape((-1))

        # 方法C
        elif method=="C":
            n1 = len(arr1_small)
            n2 = len(arr2_small)
            arr_dot_1 = np.ones(n2)
            arr_dot_2 = np.zeros(n1*n2)
            arr_dot_3 = np.hstack([arr_dot_1, arr_dot_2])
            arr_dot_4 = np.tile(arr_dot_3, reps=n1)[:n1**2*n2]
            arr_dot_5 = arr_dot_4.reshape((n1, n1*n2)).T

            arr1_rep = arr_dot_5 @ arr1_small
            arr2_rep = np.tile(arr2_small, reps=(n1, 1))
            arr_dist_reshape = np.sqrt(np.sum((arr1_rep - arr2_rep)**2, axis=1))
