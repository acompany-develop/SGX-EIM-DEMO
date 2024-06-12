# 概要
dockerを用いてクロス集計表の実行のdemoを行う．

# ディレクトリ構成
```
.
├── Dockerfile
├── README.md
├── bind
│   ├── Client0
│   │   ├── .logs
│   │   │   └── .gitkeep
│   │   ├── sample_data.csv
│   │   └── settings.ini
│   └── Client1
│       ├── .logs
│       │   └── .gitkeep
│       ├── sample_data.csv
│       └── settings.ini
└── docker-compose.yaml
```

# 実行
## 実行方法
Serverが立っている状態で，`docker-compose.yaml` を用いてコンテナを立ち上げる．  
この時，`bind/` 内の `Client{0,1}/settings.ini` を設定ファイル，`Client{0,1}/sample_data.csv` を入力ファイルとしてクロス集計表が実行される．  
実行時のログと出力結果はそれぞれ `bind/` 内の `Client{0,1}/.logs/` と `Client{0,1}/result.csv` に書き込まれる．

## オプション
### 入力ファイル
`bind/Client{0,1}/sample_data.csv` の内容を書き換えることで入力ファイルを自由に変更することが出来る．  
あるいは `docker-compose.yaml` で指定するファイルパス自体を書き換えても良い．

### 閾値

`docker-compose.yaml` に書かれている
```
./mapping settings.ini data.csv result/result.csv 5
```
の末尾の5を書き換えることで閾値を好きな値に指定出来る．（閾値については<font color="Red">todo</font>を参照）  
firm_demo0, firm_demo1 両方の閾値を同じ値にしないとエラーが出ることに注意．