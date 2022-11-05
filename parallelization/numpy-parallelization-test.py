# %%

from threadpoolctl import threadpool_info
from pprint import pp
import numpy as np

# %%
# 使用ライブラリとスレッド数の確認
pp(threadpool_info())

# %%
# numpyの設定情報を表示
np.show_config()

# %%
# 1並列の場合
from threadpoolctl import threadpool_limits
with threadpool_limits(limits=1, user_api='blas'):
    # In this block, calls to blas implementation (like openblas or MKL)
    # will be limited to use only one thread. They can thus be used jointly
    # with thread-parallelism.
    a = np.random.randn(5000, 5000)
    a_squared = a @ a

# %%
# 16並列の場合=>明らかに高速になる
with threadpool_limits(limits=16, user_api='blas'):
    a = np.random.randn(5000, 5000)
    a_squared = a @ a

