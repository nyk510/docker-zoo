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

## Usage for gpu

まずイメージを build します. yml 内では gpu の image は `machine-learning-gpu` となっているため以下のコマンドもそれに合わせています。
この名前は好きなように変更してください。

```bash
docker build -t machine-learning-gpu ./docker/gpu/
```