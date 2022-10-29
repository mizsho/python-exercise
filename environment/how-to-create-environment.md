# python環境構築メモ

異なるバージョンのpythonをpyenvで使い分ける。同じバージョンのpython環境でも、パッケージを使い分けたいのでvenvで仮想環境を作成する。Windows10 WSL2 Ubuntsu20.04で実施。

## pyenvで必要なバージョンのpythonをインストール

### pyenvを更新

現在のバージョンの`pyenv`が、欲しいpythonバージョンに対応しているか確認する。

```Shell
pyenv install --list
```

対応していない場合、`pyenv`を更新する。
※`pyenv`自体はアップデートに対応していないため、`pyenv-update`がインストールされていることが前提となる。

```Shell
pyenv update
```

### pythonをインストール

例えばpython3.11.0をインストールする場合。

```Shell
pyenv install 3.11.0
```

## venvで仮想環境を作成

### 仮想環境を作成

仮想環境を作成する。

```Shell
python -m venv venv-3110
```

仮想環境を有効化する。

```Shell
source venv-3110/bin/activate
```

### 仮想環境にパッケージをインストール

必要なパッケージをインストールする。
- `pexpect`と`ipykernel`はVSCodeで`.py`ファイルをJupyter化するのに必要。

```Shell
python -m pip install numpy pandas pexpect ipykernel
```