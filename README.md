# SGX-EIM-DEMO
# 用語

| 用語 | 説明 |
| --- | --- |
| ISV | SGXに関するリクエストを受け付けるServer |
| Firm | ISVに対してリクエストを送るClient |
| RA | Remote Attestation，SGXが安全であることを示すためのプロトコル |
| MAA | Microsoft Azure Attestation，SGXが安全であることを示すためのプロトコル |

# 動作確認済み条件

- OS
    - Ubuntu22.04
- CPU
    - 以下動作確認済み
        - Intel(R) Xeon(R) E-2288G CPU @ 3.70GHz ([Azure Standard DC4s v2](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-computing-enclaves))
        - Intel(R) Xeon(R) E-2174G CPU @ 3.80GHz (IBM Cloud)
- メモリ
    - 64GB以上 ※1
- Docker
    - Docker version 24.0.6, build ed223bc

※1 5000万件で属性パターン数100の場合、Clientの最大メモリ使用量は**約40GB**. 動作条件は以下.
- 各マッチングに使用するIDが半角英数字64文字(64bytes)以下
- 両事業者のデータ行数が5000万以下
- 両事業者の属性パターン数が100以下

# 前準備

## 設定ファイルの用意

通信や認証の設定を記載した設定ファイルを用意する．設定ファイルは事業者ごとに用意する．ファイル名や配置場所は何でも良い．フォーマットは以下の設定ファイルを参照．
- [settings_firm_a.ini](/settings/settings_firm_a.ini)
- [settings_firm_b.ini](/settings/settings_firm_b.ini)

設定ファイルのうち以下の値はServerに依存して決まるため、検証用Serverを利用したい場合はAcompanyの担当者から配布された値を設定する．

```ini
[sp]
; ServerのURLを記載する
SERVER_URL = ; 検証用環境の`SERVER_URL`が必要な場合はAcompanyの担当者に問い合わせてください。

; ISVで動作するEnclaveのMRENCLAVEとMRSIGNERを指定する。
REQUIRED_MRENCLAVE = ; 検証用環境の`REQUIRED_MRENCLAVE`が必要な場合はAcompanyの担当者に問い合わせてください。
REQUIRED_MRSIGNER = ; 検証用環境の`REQUIRED_MRSIGNER`が必要な場合はAcompanyの担当者に問い合わせてください。
```

以下のRAに関する設定は各Client個別で行う必要がある．
いくつかの値については推奨値が書き込まれている．
```ini
; Microsoft Azure Attestationの通信先URLを設定する。
; Azureで構成証明プロバイダを作成する事でURLは取得する事ができる。
MAA_URL = 

; MAAのAPIバージョンを指定する。
MAA_API_VERSIOM = 2022-08-01

; クロス集計表における行・列の選択
; 0が行（左側），1が列（上側）に対応する
CLIENT_BIT = ;0または1

; ISVに要求するEnclaveの最小ISVSVN（Security Version Number）を設定。
; ISV側はEnclave設定XMLでこれを設定できる。
MINIMUM_ISVSVN = 0

; ISVに要求するEnclaveのProduct IDを設定。
; ISV側はEnclave設定XMLでこれを設定できる。
REQUIRED_ISV_PROD_ID = 0
```


## データの用意
各事業者ごとにクロス集計表を取得するためのデータを用意する．ファイル名や配置場所は何でも良い． データの仕様は[入出力データ仕様](docs/data_in_out.md)を参照する．

# 使い方

## 動作仕様

### 引数
```console
$ ./cross_table <setting_file_name> <input_file_name> <output_file_name> <threshold>
```

- <setting_file_name: 文字列>
  - [設定ファイルの用意](#設定ファイルの用意)で用意した`.ini`設定ファイルのパスを指定
- <intput_filename: 文字列>
  - [データの用意](#データの用意)で用意した`.csv`ファイルのパスを指定
- <output_filename: 文字列>
  - 突合して生成された`.csv`形式のクロス集計表を出力するパスを指定
- <threshold: 正の整数>
  - NOTE: Firm間で同じ値を設定しないとエラーになる
  - クロス集計後のセルの値を開示する閾値`k`を設定する．`k`未満の値は全て`0`で置き換えられる
  - 入出力例は[/docs/data_in_out.md#集計数が指定した閾値に満たない](/docs/data_in_out.md#集計数が指定した閾値に満たない)を参照

### ステータスコード

| 項目 | 説明 |
| --- | --- |
| $0$ | クロス集計表が正常に出力されました． |
| $134$ |エラーが発生しました． |


### エラーメッセージ
[動作上の注意点](#動作上の注意点)に記載されている内容以外のエラーメッセージが出るケース．原因を示す行は必ず`ERROR:`で始まっている．

**引数の個数が間違っている場合**
```bash
ERROR: Usage: ./cross_table <setting_file_name> <intput_filename> <output_filename> <threshold>
```
**threshold として非負整数以外を入力した場合**
```bash
ERROR: Threshold must be nonnegative integer.
```
**input_filename として存在しないfileのpathを指定した場合**
```bash
ERROR: Input file does not exist.
```
**settings_fileの内容に不備があった場合**
```bash
 INFO: Start settings load.
ERROR: # 不備の内容に対応するメッセージ
```
不備がなかった場合は以下のように表示される．
```bash
 INFO: Start settings load.
 INFO: Successfully loaded settings.
```
**RA 失敗時**
```bash
ERROR: RA failed. Clean up and exit program.
```
この場合は失敗の原因によってこのメッセージのさらに数行上に表示されるログの内容が異なる．

ISVが落ちている状態で投げた場合
```bash
ERROR: Unknown error. Probably SGX server is down.
```
`settings_file`の`REQUIRED_MRENCLAVE`の値が間違っている場合
```bash
ERROR: MRENCLAVE mismatched. Reject RA.
```
`settings_file`の`REQUIRED_MRSIGNER`の値が間違っている場合
```bash
ERROR: MRSIGNER mismatched. Reject RA.
```


# 実行方法

各事業者ごとにFirmを起動させてクロス集計表を計算する．
実行方法はバイナリを実行する方法と、Dockerを利用する方法の2パターンある．

**※ 実際にISVに対して通信しにいくため事前にISVが起動していることをISV管理者に確認する．**


## 直接バイナリを実行する場合
実行するためのバイナリとIASのReport署名ルートCA証明書ファイルが必要なのでそれぞれwgetなどでDownloadする．
これらのファイルは同一のディレクトリに配置する．

```console
$ export VERSION=<任意のバージョンを指定>
$ wget https://certificates.trustedservices.intel.com/Intel_SGX_Attestation_RootCA.pem
$ wget https://github.com/acompany-develop/SGX-EIM-DEMO/releases/download/${VERSION}/SGX-EIM-v${VERSION}-linux-x64.zip
$ unzip SGX-EIM-v${VERSION}-linux-x64.zip
```

unzipすると同じディレクトリ内に`cross_table`という実行バイナリがあるので以下のコマンドで実行する．

```console
# 事業者A
$ ./cross_table ./settings/settings_firm_a.ini ./data/sample_data1.csv ./result/result1.csv 3
```

## docker-compose上でバイナリを実行する場合
本リポジトリ内に`docker-compose.yaml`のサンプルがあるため，Cloneしたのちこれを編集して実行する．
```console
# リポジトリのClone
$ git clone https://github.com/acompany-develop/SGX-EIM-DEMO.git
```
docker-compose.yaml
```yaml
version: '3.3'

x-build: &build
  build:
    context: .
    dockerfile: Dockerfile
    args:
      VERSION: "<ISVと同じバージョン>"

services:
  firm_demo:
    <<: *build
    volumes:
    - type: bind
      source: <Step2で作成した設定ファイルの相対パス> 
      target: /settings.ini
    - type: bind
      source: <Step3で作成したデータの相対パス> 
      target: /data.csv
    - type: bind
      source: <計算結果を保存したいパス>
      target: /result
    command:
      - /bin/bash
      - '-c'
      - ./cross_table settings.ini data.csv result/result.csv 3
```

準備ができたらdocker composeコマンドで起動する．

```console
$ docker-compose up firm_demo
```

## デモ

### 直接バイナリで事業者A,BのFirmを実行する場合

別々のterminalから以下のコマンドを実行すると，正常に処理が完了すると`result/result{1,2}.csv`に出力データが生成される．

```console
# 事業者A
$ ./cross_table ./settings/settings_firm_a.ini ./data/sample_data1.csv ./result/result1.csv 3
# 事業者B
$ ./cross_table ./settings/settings_firm_b.ini ./data/sample_data2.csv ./result/result2.csv 3
```

### docker-compose上で事業者A,BのFirmを実行する

docker composeのserviceを1つ増やして同時に起動すれば良い．[SGX-EIM-DEMO/docker-compose.yaml](docker-compose.yaml)では動作確認用に最初から2つのserviceがあるため以下のコマンドでそのまま実行可能．

```yaml
version: '3.3'

services:
  firm_demo1:
    # 中略
  firm_demo2:
    # 中略(パスはfirm_demo1と異なるはずなので注意)
```

```console
$ docker-compose up firm_demo1 firm_demo2
```

## 動作上の注意点

### 両事業者が実行しなければ動作が終了しない

クロス集計表は2つの事業者がデータを送信して初めて計算が行われる．そのため，片方の事業者だけが処理を実行した場合，永遠に計算が終わらず待機し続けてしまう．その場合は下記のログが出続けることになる．

```bash
INFO: ==============================================
INFO: Get Execute Status
INFO: ==============================================
```

### 両事業者が異なる設定で動作させることはできない

クロス集計表の閾値は自由に設定することができるが，両事業者が異なる値を設定した場合は処理が失敗する．その場合は次のいずれかのログが出る．

```bash
ERROR: Fail get execute status with 'Threshold values inputtedare different.'.
```

```bash
ERROR: Fail eim request with 'Threshold values inputted are different.'.
```

### 同一事業者は同時に実行できない（同時実行数が1リクエスト）

リクエスト送信後にリクエストを終了させずにもう一度リクエストを送信した場合，先に送った方に影響はなく後に送った方のみ失敗する．その場合は次のログが出る．
ISVのEnclaveの制約により複数の処理を同時に捌けないため同時実行数が1リクエストのみという制限がある．

```bash
ERROR: Fail eim request with 'This firm has already sent a request.'.
```

### サーバを再起動させる
想定外挙動によりサーバがリクエストを正しく捌けなくなった場合，以下のように`/stop` APIを叩くことでサーバを再起動できる．
```console
$ curl <IP>:<port>/stop
```
このリクエストも通らない場合は手動でサーバを再起動させる必要があるため管理者に連絡する．


## その他のAPI
### /info
ISVサーバの状態を取得できる．
```console
$ curl <IP>:<port>/info
{
  "health" : "healthy",
  "version" : "v1.0.1"
}
```
### /stop
ISVサーバを停止できる．何らかの問題が発生した場合に再起動させるために使える．
```console
$ curl <IP>:<port>/stop
```
