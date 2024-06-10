# 概要
v1.6.0 で追加された `mapping` バイナリの `cross_table` バイナリとの差分を記載．  
ここに書いてある内容は `cross_table` バイナリが廃止される v2.0.0 で移動される予定．


# ディレクトリ概要
```
.
├── data_in_out.md               # 入出力の基本形式について
├── guarantee.md               # 入力ファイルの動作保証条件について
```
# cross_table との差分について
`cross_table` と `mapping` は入力ファイル・出力ファイルの形式が異なるだけで，動作確認済条件や設定ファイルなどに関しては同じである．  
こちらについては [../README.md](../README.md) などを参考．

実行方法もコマンドの形式が
```console
# 事業者A
$ ./cross_table ./settings/settings_firm_a.ini ./data/sample_data1.csv ./result/result1.csv 3
# 事業者B
$ ./cross_table ./settings/settings_firm_b.ini ./data/sample_data2.csv ./result/result2.csv 3
```
から
```console
# 事業者A
$ ./mapping ./settings/settings_firm_a.ini ./data/sample_data1.csv ./result/result1.csv 3
# 事業者B
$ ./mapping ./settings/settings_firm_b.ini ./data/sample_data2.csv ./result/result2.csv 3
```
に変わったことと，入力ファイルの形式が変更した以外は同じである．  
したがって [両事業者が実行しなければ動作が終了しない](../README.md#両事業者が実行しなければ動作が終了しない) や [両事業者が異なる設定で動作させることはできない](../README.md#両事業者が異なる設定で動作させることはできない) などの制約は依然として存在する．  

また，Server は `cross_table` と `mapping` のリクエストを同時に捌くことが出来ない．  
例えば事業者Aが
```console
$ ./cross_table ./settings/settings_firm_a.ini ./data/sample_data1.csv ./result/result1.csv 3
```
を実行したのち，事業者Bが
```console
$ ./mapping ./settings/settings_firm_b.ini ./data/sample_data2.csv ./result/result2.csv 3
```
を実行した場合，（事業者A側のリクエストには影響はなく）事業者B側に以下のエラーメッセージが表示される．
```
2024-06-10 05:47:01 +0000 | FATAL: | CHALLENGE  | client_app.cpp:main_process_map - AssertionError: Queries are different : the other's query is {"query_type" : "Cross", "threshold" : 3}
```
