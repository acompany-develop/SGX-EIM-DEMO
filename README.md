# SGX-EIM-DEMO
# 用語

| 用語 | 説明 |
| --- | --- |
| ISV | SGXに関するリクエストを受け付けるServer |
| Firm | ISVに対してリクエストを送るClient |
| RA | Remote Attestation，SGXが安全であることを示すためのプロトコル |
| MAA | Microsoft Azure Attestation，SGXが安全であることを示すためのプロトコル |

# ディレクトリ概要
```
.
├── .logs/ #                        # Firmデモ実行ログファイル出力先
│   ├── firm_demo1/                 # firm_demo1用
│   └── firm_demo2/                 # firm_demo1用
├── data/                           # docker-compose.yamlの実行時ログファイル出力先
│   ├── sample_data1.csv            # firm_demo1用
│   └── sample_data2.csv            # firm_demo2用
├── docs/                           # Firmについてのドキュメント置き場
├── guarantee/                      # Firm動作保証についてのドキュメント置き場
├── map/                            # v1.6.0 で追加されたmap形式のバイナリについてのドキュメント置き場  
├── licenses/
├── result/                         # Firmデモ用 出力結果csv置き場
├── settings/                       # Firmデモ用 settingsファイル置き場
│   ├── settings_client_a.ini       # firm_demo1用
│   └── settings_client_b.ini       # firm_demo2用
├── docker-compose.yaml             # Firmデモ用docker-compose.yaml
├── Dockerfile                      # Firmデモ用Dockerfile
└── README.md
```

# 動作確認済み条件

- OS
    - Ubuntu22.04
- CPU
    - 以下動作確認済み
        - Intel(R) Xeon(R) E-2288G CPU @ 3.70GHz ([Azure Standard DC4s v2](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-computing-enclaves))
        - Intel(R) Xeon(R) E-2174G CPU @ 3.80GHz (IBM Cloud)
- メモリ
    - 64GB以上 ※1


※1 5000万件で属性パターン数100の場合、Clientの最大メモリ使用量は**約40GB**. 動作条件は以下.
- 各マッチングに使用するIDが半角英数字64文字(64bytes)以下
- 両事業者のデータ行数が5000万以下
- 両事業者の属性パターン数が100以下

入力csvの詳しい動作保証要件は[guarantee](./guarantee/README.md)を参照．

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
[動作上の注意点](#動作上の注意点)に記載されている内容以外のエラーメッセージが出るケース．原因を示す行は`ERROR:`を含む以下のformatで出力される．
```bash
<timestamp> | ERROR: | <type> | <file>:<function> - <target> | <error message>
```
以下では`<error message>`のみ抜粋する．

**引数の個数が間違っている場合**
```bash
ValidationError: Usage: ./cross_table <setting_file_name> <input_file_name> <output_file_name> <threshold>
```
**threshold として非負整数以外を入力した場合**
```bash
ValidationError: Threshold must be nonnegative integer.
```
**input_filename として存在しないfileのpathを指定した場合**
```bash
ValidationError: Input file does not exist.
```
** input_fileにデータが存在しない場合
```bash
ValidationError: There is no data.
```
**input_fileの行数が5000万行より多い場合**
```bash
ValidationError: The number of rows of data exceeds 50 million.
```
**input_fileのid列の長さが65文字以上の場合**
```bash
ValidationError: Line 1 has the key which length exceeds 64.
```
**input_fileの属性列の長さが65文字以上の場合**
```bash
ValidationError: Line 1 has the attribute which length exceeds 64.
```
**input_fileに使用不可の文字が含まれる場合**
```bash
ValidationError: Line 1 contains ' '
```
**input_fileに共通のIDが含まれる場合**
```bash
ValidationError: There are multiple data with key "<共通のID>"
```
**input_fileの属性種類数が100より多い場合**
```bash
ValidationError: Number of attribute types exceeds 100.
```
**input_fileのid列が空の場合**
```bash
ValidationError: Line 1 has empty key.
```
**input_fileの属性列が空の場合**
```bash
ValidationError: Line 1 has empty attribute.
```
**input_fileのid列,属性列が空の場合**
```bash
ValidationError: data.csv Line 1 has no comma.
```
**settings_fileの内容に不備があった場合**
```bash
ValidationError: # 不備の内容に対応するメッセージ
```
**RA 失敗時**
```bash
AssertionError: Fail ra
```

ISVが落ちている状態で投げた場合
```bash
HttpException: Unknown error. Probably SGX server is down. | null | <method> <pattern> | <request parameters>
```
`settings_file`の`REQUIRED_MRENCLAVE`の値が間違っている場合
```bash
ValidationError: MRENCLAVE mismatched. Reject RA.
```
`settings_file`の`REQUIRED_MRSIGNER`の値が間違っている場合
```bash
ValidationError: MRSIGNER mismatched. Reject RA.
```


# 実行方法

各事業者ごとにFirmを起動させてクロス集計表を計算する．

**※ 実際にISVに対して通信しにいくため事前にISVが起動していることをISV管理者に確認する．**


## バイナリを実行する方法
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

## デモ

### 直接バイナリで事業者A,BのFirmを実行する場合

別々のterminalから以下のコマンドを実行すると，正常に処理が完了すると`result/result{1,2}.csv`に出力データが生成される．

```console
# 事業者A
$ ./cross_table ./settings/settings_firm_a.ini ./data/sample_data1.csv ./result/result1.csv 3
# 事業者B
$ ./cross_table ./settings/settings_firm_b.ini ./data/sample_data2.csv ./result/result2.csv 3
```

## 動作上の注意点

### 両事業者が実行しなければ動作が終了しない

クロス集計表は2つの事業者がデータを送信して初めて計算が行われる．そのため，片方の事業者だけが処理を実行した場合，永遠に計算が終わらず待機し続けてしまう．

### 両事業者が異なる設定で動作させることはできない

クロス集計表の閾値は自由に設定することができるが，両事業者が異なる値を設定した場合は処理が失敗する．その場合は次のいずれかのログが出る．

```bash
HttpException: Threshold values inputted are different. | 500 | POST /eim-request | <request parameters>
```

### 同一事業者は同時に実行できない（同時実行数が1リクエスト）

リクエスト送信後にリクエストを終了させずにもう一度リクエストを送信した場合，先に送った方に影響はなく後に送った方のみ失敗する．その場合は次のログが出る．
ISVのEnclaveの制約により複数の処理を同時に捌けないため同時実行数が1リクエストのみという制限がある．
すでにServerにリクエストを送信したかどうかは[/info](#info) APIから確認できる．

```bash
HttpException: This client has already sent a request. | 500 | <method> <pattern> | <request parameters>
```
### サーバを再起動させる
想定外挙動によりサーバがリクエストを正しく捌けなくなった場合，サーバは自動で再起動されて正常な状態に戻る．
再起動されず異常な挙動を起こし続ける場合は以下のように`/stop` APIを叩くことでClient側からサーバを再起動できる．
```console
$ curl <IP>:<port>/stop
```
このリクエストも通らない場合は手動でサーバを再起動させる必要があるため管理者に連絡する．

### 実行中の処理を強制終了した場合
クライエントがCtrl+Cなどによって処理を途中で終了させた場合，サーバがリクエストを正しく捌けなくなることがある．
異常な挙動が起きた場合は，[サーバを再起動させる](./README.md#サーバを再起動させる)に記載の通り サーバは自動で再起動されて再起動することで正常状態に戻る．

## その他のAPI
### /info
ISVサーバの状態を取得できる．
`server_state`の説明は[server_state.md](docs/server_state.md)を参照．
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

### /stop
ISVサーバを停止できる．何らかの問題が発生した場合に再起動させるために使える．
```console
$ curl <IP>:<port>/stop
```

# 備考
> [!IMPORTANT]
> Firmは実行時に標準出力とファイル出力でログを出力するが，ファイル出力先はbinary実行ディレクトリ内の`.logs/`ディレクトリに固定されている．障害調査時に`.logs/`の提出を依頼する可能性がある．

> [!IMPORTANT]
> ISVへの同一IPからのリクエストは1分あたり60回までとする. <br>
> 60回より多くリクエストを送ると`403 Forbidden`が返される.
