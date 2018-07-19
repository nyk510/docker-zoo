# Machine Learning

機械学習用の docker ファイル及び docker-compose を配置するディレクトリ

## Pre Requirements

このディレクトリの docker-compose では version 2.3 形式で yml を記述しています。  
これは gpu を有効化した docker を作る際 runtime オプションを使うためです。 `runtime: nvidia`

そのためちょっと古い docker-compose では動かないかも知れません.
筆者の環境は以下のようになっています

```bash
➜ docker-compose --version
docker-compose version 1.19.0, build 9e633ef

➜ docker version
Client:
 Version:      18.03.1-ce
 API version:  1.37
 Go version:   go1.9.5
 Git commit:   9ee9f40
 Built:        Thu Apr 26 07:17:20 2018
 OS/Arch:      linux/amd64
 Experimental: false
 Orchestrator: swarm

Server:
 Engine:
  Version:      18.03.1-ce
  API version:  1.37 (minimum version 1.12)
  Go version:   go1.9.5
  Git commit:   9ee9f40
  Built:        Thu Apr 26 07:15:30 2018
  OS/Arch:      linux/amd64
  Experimental: false
```

## Usage

~ つかいかた

### CPU Version

以下のライブラリがインストールされた環境が構築されます

* python
  * miniconda3-4.1.11
* packages:
  * xgboost
  * lightGBM
  * jupyter
  * notebook
  * tqdm
  * matplotlib
  * numpy
  * scipy
  * scikit-learn
  * pandas
  * numba

### GPU Version

> note: compose を動かすためには `nvidia-docker2` が必要です。

GPUバージョンは基本的にCPUと同じですが

* lightGBM
* xgboost
* keras (backend: tensorflow-gpu)

の各ライブラリが GPU 対応となります。

まずイメージを build します. yml 内では gpu の image は `machine-learning-gpu` となっているため以下のコマンドもそれに合わせています。
この名前は好きなように変更してください。

```bash
docker build -t machine-learning-gpu ./docker/gpu/
```

次に env ファイルを作成します

```bash
cp sample.env .env
```

env ファイル内では jupyter のポート番号とコンテナの名前を設定します。

最期に gpu 用の compose ファイルをコピーしてコンテナを起動します

```bash
cp docker-compose.gpu.yml docker-compose.yml
docker-compose up -d
```

デフォルトならば [localhost ポート番号 4000](http://localhost:4000/tree?) にサーバーが立ち上がります

> ちなみに compose ファイルは santander コンペ仕様になっているので jupyter で開いたルートディレクトリの data には santander のデータセットが保存されています

### 注意

この compose ファイル及び docker image は本番利用しないでください。  
コンテナ内部のユーザーが root のままになっていますので乗っ取られた場合それなりのリスクです。
