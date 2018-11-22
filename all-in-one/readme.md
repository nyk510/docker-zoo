# All In One

miniconda(python3) + 解析ツール + NLP Tool(Mecab) + Noto Font

## Quick Start

```bash
docker-compose build
docker-compose up -d
```

[localhost:6001](http://localhost:6001/) に jupyter が開きます. パスワードは Dockerfile を参照のこと.

## MySQL との接続

`project.env` を `.env` にコピーした後必要な情報を入力してください.

```env
MYSQL_HOST=
MYSQL_URERNAME=
MYSQL_PASSWORD=

MYSQL_PORT=3306
MYSQL_DB_NAME=
```