# 並列処理のメモ

## `numpy`

そもそも前提として`numpy`で完結するような処理は並列処理される。
メモリが足りず小分けにして処理するしかない計算の場合が問題になる。

### `numpy`で使われるスレッド数やライブラリを確認

- スレッド数や使用ライブラリの確認は`threadpoolctl`で可能。
インポートされたライブラリの情報が表示される。
`'num_threads': 16`、`'internal_api': 'openblas'`と表示された。

    ```python
    from threadpoolctl import threadpool_info
    import numpy as np
    threadpool_info()
    ```

- 環境変数を用いたスレッド数の制御はこの解説記事が参考になりそう。

    https://qiita.com/yymgt/items/b7f151ee99fb830ca64c

- `threadpoolctl`で直接スレッド数の設定が可能。

    ```python
    from threadpoolctl import threadpool_limits
    with threadpool_limits(limits=1, user_api='blas'):
    ```

## `multiprocessing`

参考になりそうなサイト
- https://note.com/npaka/n/na95cfc0e494d#lumk6

### sleep関数のテスト

意図通り並列的に動作することを確認。

### 座標間の距離を計算する関数(numpy)のテスト

並列化しない場合より時間がかかってしまう。理由は不明。

並列化すると、複数のコアでCPU使用率が上昇することを確認。

並列化はせずに`Process`を使うだけで2.5s⇒41.5sと大幅に時間がかかってしまう。ndarrayのビューを引数に渡しているので大丈夫と思っていたが、実はメモリが共有できていないため？

## `concurrent`

### sleep関数のテスト

意図通り並列的に動作することを確認。

投入したスレッドが終了するまで待つのに、`as_completed`がうまく機能しない。
`wait`を試したところ待機させることに成功。

### 座標間の距離を計算する関数(numpy)のテスト

並列化(`max_workers=2`)でわずかに速くなることを確認。
しかし、並列数を増やすと時間がかかってしまう。原因は不明。メモリが共有できておらず新たなメモリを確保する際のオーバーヘッドが律速している？`ThreadPoolExecutor`(マルチスレッド処理：メモリを共有する)より`ProcessPoolExecutor`(マルチプロセス処理：メモリを共有しない)のほうが遅い。