# 概要
Client 側に出るエラーメッセージとその考えられる原因について解説する．

原因を示す行は`ERROR:`を含む以下のformatで出力される．
```
<timestamp> | ERROR: | <type> | <file>:<function> - <target> | <error message>
```
以下では`<error message>`のみ抜粋する．
# エラーメッセージ
**引数の個数が間違っている場合**
```
ValidationError: Usage: ./mapping <setting_file_name> <input_file_name> <output_file_name> <threshold>
```
**threshold として非負整数以外を入力した場合**
```
ValidationError: Threshold must be nonnegative integer.
```
**input_filename として存在しないfileのpathを指定した場合**
```
ValidationError: Input file does not exist.
```
**input_fileにデータが存在しない場合**
```
ValidationError: There is no data.
```
**input_fileの行数が5000万行より多い場合**
```
ValidationError: The number of rows of data exceeds 50 million.
```
**input_fileのid列の長さが65文字以上の場合**
```
ValidationError: Line 1 has the key which length exceeds 64.
```
**input_fileの属性列の長さが65文字以上の場合**
```
ValidationError: Line 1 has the attribute which length exceeds 64.
```
**input_fileに使用不可の文字が含まれる場合**
```
ValidationError: Line 1 contains ' '
```
**input_fileに共通のIDが含まれる場合**
```
ValidationError: There are multiple data with key "<共通のID>"
```
**input_fileの属性種類数が100より多い場合**
```
ValidationError: Number of attribute types exceeds 100.
```
**input_fileのid列が空の場合**
```
ValidationError: Line 1 has empty key.
```
**input_fileの属性列が空の場合**
```
ValidationError: Line 1 has empty attribute.
```
**input_fileのid列,属性列が空の場合**
```
ValidationError: data.csv Line 1 has no comma.
```
**settings_fileの内容に不備があった場合**
```
ValidationError: # 不備の内容に対応するメッセージ
```
**RA 失敗時**
```
AssertionError: Fail ra
```

**ISVが落ちている状態で投げた場合**
```
HttpException: Unknown error. Probably SGX server is down. | null | <method> <pattern> | <request parameters>
```
**`settings_file`の`REQUIRED_MRENCLAVE`の値が間違っている場合**
```
ValidationError: MRENCLAVE mismatched. Reject RA.
```
**`settings_file`の`REQUIRED_MRSIGNER`の値が間違っている場合**
```
ValidationError: MRSIGNER mismatched. Reject RA.
```