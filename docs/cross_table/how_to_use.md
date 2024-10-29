# 概要
クロス集計表を実行する方法について記載．  
Dockerによるデモを実行する [demo_docker](../../demo_docker/README.md) も参考．

ISVサーバが立ち上がっている状態で2つのFirmがそれぞれ実行する必要があることに注意．

# 前準備
## 設定ファイルの用意

通信や認証の設定を記載した設定ファイルを用意する．
設定ファイルは事業者ごとに用意する．
ファイル名や配置場所は何でも良い．

フォーマットはdemo_dockerの設定ファイルを参照．
- [settings.ini](../../demo_docker/bind/Client0/settings.ini)

設定ファイルのうち以下の値はISVサーバに依存して決まるため、検証用ISVサーバを利用したい場合はAcompanyの担当者から配布された値を設定する．

```ini
[sp]
; ISVのURLを記載する
SERVER_URL = ; 検証用環境の`SERVER_URL`が必要な場合はAcompanyの担当者に問い合わせてください。

; ISVで動作するEnclaveのMRENCLAVEとMRSIGNERを指定する。
REQUIRED_MRENCLAVE = ; 検証用環境の`REQUIRED_MRENCLAVE`が必要な場合はAcompanyの担当者に問い合わせてください。
REQUIRED_MRSIGNER = ; 検証用環境の`REQUIRED_MRSIGNER`が必要な場合はAcompanyの担当者に問い合わせてください。

[AuthorizationAuthentication]
CLIENT_ID_FOR_FIRM_TO_PETS_AUTHORIZATION = ; 検証用環境の`CLIENT_ID_FOR_FIRM_TO_PETS_AUTHORIZATION`が必要な場合はAcompanyの担当者に問い合わせてください。
CLIENT_SECRET_FOR_FIRM_TO_PETS_AUTHORIZATION = ; 検証用環境の`CLIENT_SECRET_FOR_FIRM_TO_PETS_AUTHORIZATION`が必要な場合はAcompanyの担当者に問い合わせてください。
GRANT_TYPE_FOR_CLIENT_CREDENTIALS_FLOW = ; 検証用環境の`GRANT_TYPE_FOR_CLIENT_CREDENTIALS_FLOW`が必要な場合はAcompanyの担当者に問い合わせてください。
AUDIENCE = ; 検証用環境の`AUDIENCE`が必要な場合はAcompanyの担当者に問い合わせてください。
AUTH_SERVER_URL = ; 検証用環境の`AUTH_SERVER_URL`が必要な場合はAcompanyの担当者に問い合わせてください。
TOKEN_ENDPOINT = ; 検証用環境の`TOKEN_ENDPOINT`が必要な場合はAcompanyの担当者に問い合わせてください。
CONTENT_TYPE = ; 検証用環境の`CONTENT_TYPE`が必要な場合はAcompanyの担当者に問い合わせてください。
ISSUER = ; 検証用環境の`ISSUER`が必要な場合はAcompanyの担当者に問い合わせてください。
PUBLIC_KEYS_URL = ; 検証用環境の`PUBLIC_KEYS_URL`が必要な場合はAcompanyの担当者に問い合わせてください。
```

以下のRAに関する設定は各Firmが個別で行う必要がある．
いくつかの値については推奨値が書き込まれている．
```ini
; Microsoft Azure Attestationの通信先URLを設定する。
; Azureで構成証明プロバイダを作成する事でURLは取得する事ができる。
MAA_URL =

; MAAのAPIバージョンを指定する。
MAA_API_VERSIOM = 2022-08-01

; ISVが二つのFirmを見分けるためのID
; 出力ファイルのheaderにも仕様される
CLIENT_BIT = ;0または1

; ISVに要求するEnclaveの最小ISVSVN（Security Version Number）を設定。
; ISV側はEnclave設定XMLでこれを設定できる。
MINIMUM_ISVSVN = 0

; ISVに要求するEnclaveのProduct IDを設定。
; ISV側はEnclave設定XMLでこれを設定できる。
REQUIRED_ISV_PROD_ID = 0
```

## データの用意
各事業者ごとにクロス集計表を取得するためのデータを用意する．
ファイル名や配置場所は何でも良い． 

データの形式 : [data_in_out.md](./data_in_out.md)  
データの詳しい動作保証要件 : [guarantee.md](./guarantee.md)

## バイナリなどの取得
実行するためのバイナリとIASのReport署名ルートCA証明書ファイルが必要なのでそれぞれwgetなどでDownloadする．
これらのファイルは同一のディレクトリに配置する．

```console
$ export VERSION=<任意のバージョンを指定>
$ wget https://certificates.trustedservices.intel.com/Intel_SGX_Attestation_RootCA.pem
$ wget https://github.com/acompany-develop/SGX-EIM-DEMO/releases/download/${VERSION}/SGX-EIM-v${VERSION}-linux-x64.zip
$ unzip SGX-EIM-v${VERSION}-linux-x64.zip
```
# 実行
**※ 実際にISVに対して通信しにいくため事前にISVが起動していることをISV管理者に確認する．**

[バイナリなどの取得](#バイナリなどの取得)で取得した `cross_table` バイナリを以下のコマンドで実行する．
```console
$ ./cross_table <setting_file_name> <input_file_name> <output_file_name> <threshold>
```
## 引数
- <setting_file_name: 文字列>
  - [設定ファイルの用意](#設定ファイルの用意)で用意した`.ini`設定ファイルのパスを指定
- <intput_filename: 文字列>
  - [データの用意](#データの用意)で用意した`.csv`ファイルのパスを指定
- <output_filename: 文字列>
  - 突合して生成された`.csv`形式のクロス集計表を出力するファイルのパスを指定
- <threshold: 正の整数>
  - NOTE: Firm間で同じ値を設定しないとエラーになる
  - クロス集計後のセルの値を開示する閾値`k`を設定する  
    `k`未満の値は全て`0`で置き換えられる


## ステータスコード

| 項目 | 説明 |
| --- | --- |
| $0$ | クロス集計表が正常に出力されました． |
| $134$ |エラーが発生しました． |

## 実行時の注意
### 両事業者が実行しなければ動作が終了しない
クロス集計表は2つの事業者がデータを送信して初めて計算が行われる．
そのため，片方の事業者だけが処理を実行した場合，永遠に計算が終わらず待機し続けてしまう．

### 両事業者が異なる設定で動作させることはできない
クロス集計表の閾値は自由に設定することができるが，両事業者が異なる値を設定した場合は処理が失敗する．
その場合は次のいずれかのログが出る．

```bash
HttpException: Threshold values inputted are different. | 500 | POST /eim-request | <request parameters>
```

### 同一事業者は同時に実行できない（同時実行数が1リクエスト）
リクエスト送信後にリクエストを終了させずにもう一度リクエストを送信した場合，先に送った方に影響はなく後に送った方のみ失敗する．その場合は次のログが出る．
ISVサーバのEnclaveの制約により複数の処理を同時に捌けないため同時実行数が1リクエストのみという制限がある．
すでにISVにリクエストを送信したかどうかは[/info](#info) APIから確認できる．

```bash
HttpException: This client has already sent a request. | 500 | <method> <pattern> | <request parameters>
```
### 実行中の処理を強制終了した場合
クライエントがCtrl+Cなどによって処理を途中で終了させた場合，サーバがリクエストを正しく捌けなくなることがある．
異常な挙動が起きた場合は，[/stop](#stop) API を用いてサーバを停止させる．
停止したサーバは自動で再起動されて正常状態に戻る．

このリクエストも通らない場合は手動でサーバを再起動させる必要があるため管理者に連絡する．

# API
## /info
ISVサーバの状態を取得できる．
`server_state`の説明は[server_state.md](./server_state.md)を参照．
以下の例は成形されたものであり，実際には１行で出力される．
```console
$ curl <IP>:<port>/info
{
	"health": "healthy",
	"server_state": {
		"client0": {
			"message": "Initialized",
			"status_code": 0
		},
		"client1": {
			"message": "Initialized",
			"status_code": 0
		}
	},
	"version": "v1.4.0"
}
```
## /stop
ISVサーバを停止できる．
停止したサーバは自動で再起動されるため，[実行中の処理を強制終了した場合](#実行中の処理を強制終了した場合) などサーバの状態をリセットしたい時に使う．
```console
$ curl <IP>:<port>/stop
```
FirmがISVに送っていたリクエストなどがリセットされるため，使用する時は事前に他のFirmと認識をそろえることを推奨する．


# 備考
> <font color="Red">[!IMPORTANT]</font>  
> Firmは実行時に標準出力とファイル出力でログを出力するが，ファイル出力先はbinary実行ディレクトリ内の`.logs/`ディレクトリに固定されている．障害調査時に`.logs/`の提出を依頼する可能性がある．

> <font color="Red">[!IMPORTANT]</font>  
> ISVへの同一IPからのリクエストは1分あたり60回までとする. <br>
> 60回より多くリクエストを送ると`403 Forbidden`が返される.