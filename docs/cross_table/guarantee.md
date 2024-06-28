# 概要
入力するcsvに関して動作保証されている要件を記載．  
入力形式については [data_in_out.md](data_in_out.md) を参照．  
動作保証環境については [動作確認済み条件](../../README.md#動作確認済み条件) を参照
# csv要件
* 行数5千万以下
* 属性数の上限制約無し（v2.0.0以降）
* headerは[利用可能文字](#利用可能文字)から構成される長さ1以上140以下の文字列
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
## header が140文字を超えている
```csv
mail_address,sex,height,age,weight,country,state,city,zipcode,occupation,education_level,marital_status,number_of_children,favorite_color,hobbies,membership_status,subscription_type,preferred_language
g1@mail.com,M,170,25,70,USA,CA,Los Angeles,90001,Engineer,Bachelor's,Single,0,Blue,Reading,Gold,Monthly,English
g2@mail.com,F,160,30,55,Canada,ON,Toronto,M5H,Doctor,PhD,Married,2,Green,Traveling,Platinum,Yearly,French
g3@mail.com,M,180,22,80,UK,LN,London,E1 6AN,Artist,Master's,Single,0,Red,Drawing,Silver,Monthly,Spanish
g4@mail.com,F,155,28,50,Australia,NSW,Sydney,2000,Lawyer,Bachelor's,Married,3,Yellow,Cooking,Gold,Yearly,English
g5@mail.com,M,175,35,85,Germany,BY,Munich,80331,Scientist,PhD,Single,0,Black,Hiking,Platinum,Monthly,German
```
header の合計長が200文字あり，140文字を超えている．  
header : `mail_address,sex,height,age,weight,country,state,city,zipcode,occupation,education_level,marital_status,number_of_children,favorite_color,hobbies,membership_status,subscription_type,preferred_language`
## ID列が64文字を超えている
```csv
mail_address,age
very_very_long_email_address_that_is_quite_impressive@example.com,20
short@example.com,10
```
2行目のIDが65文字あり，64文字を超えている．  
2行目のID : `very_very_long_email_address_that_is_quite_impressive@example.com`

## 属性列が64文字を超えている
```csv
mail_address,Age,Country,Proverb
alexandria.johnson123@example.com,28,United States of America,A journey of a thousand miles begins with a single step.
bfranklin456@example.com,34,United Kingdom of Great Britain and Northern Ireland,Time is money.
charlotte.williams789@example.com,22,Canada,Actions speak louder than words.
eduardo.schmidt202@example.com,40,Federal Republic of Germany,The early bird catches the worm.
```
2行目の属性列が84文字あり，64文字を超えている．  
2行目の属性列 : `28,United States of America,A journey of a thousand miles begins with a single step.`

## 同じIDを持つ行がある
```csv
mail_address,Age,Country
apple@example.com,20,Japan
banana@example.com,10,America
apple@example.com,15,China
grape@example.com,20,America
```
2行目と4行目のID列が一致している．  
2行目と4行目のID列 : `apple@example.com`

## 利用可能文字以外の文字を使っている
```csv
mail_address,年齢,Country
apple@example.com,20,Japan
banana@example.com,10,America
grape@example.com,20,America
```
header に利用可能文字以外の文字を使っている