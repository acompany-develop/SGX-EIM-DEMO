# 概要
入力するcsvに関して動作保証されている要件を記載．  
入力形式については [data_in_out.md](data_in_out.md) を参照．  
動作保証環境については [動作確認済み条件](../../README.md#動作確認済み条件) を参照
# csv要件
* 行数5千万以下
* 属性数の上限制約無し（v2.0.0以降）
* headerは[利用可能文字](#利用可能文字)から構成される長さ1以上140以下の文字列．
* ID列と属性列はそれぞれ[利用可能文字](#利用可能文字)から構成される長さ1以上64以下の文字列
* ID列と属性列は`,`で区切り，間や末尾にスペースを入れない
* ID列に`,`は利用不可（`,`はID列と属性列の境界文字として解釈されるため）
* 異なる行で共通のIDを持つものがあってはならない
# 利用可能文字
[graphical representation](https://en.cppreference.com/w/cpp/string/byte/isgraph)で定義されたもの．
```
digits (0123456789)
uppercase letters (ABCDEFGHIJKLMNOPQRSTUVWXYZ)
lowercase letters (abcdefghijklmnopqrstuvwxyz)
punctuation characters (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
```

# 動作保証されていないcsvの例
<font color="Red">todo</font>