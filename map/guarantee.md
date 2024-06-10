# 動作保証について
入力するcsvに関して動作保証されている要件
入力形式については [入出力データ仕様](data_in_out.md) を参照 
## csv要件
* 行数1千万以下
* ID列と属性列は利用可能な文字から構成される長さ1以上64以下の文字列
* ID列と属性列はカンマ（,）で区切り，間や末尾にスペースを入れない
* ID列に`,`は利用不可（`,`はID列と属性列の境界文字として解釈されるため）
* 異なる行で共通のIDを持つものがあってはならない
* 利用可能文字は[graphical representation](https://en.cppreference.com/w/cpp/string/byte/isgraph)で定義されたもの．
```
digits (0123456789)
uppercase letters (ABCDEFGHIJKLMNOPQRSTUVWXYZ)
lowercase letters (abcdefghijklmnopqrstuvwxyz)
punctuation characters (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
```