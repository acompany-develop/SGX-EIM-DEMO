# 動作保証について
入力するcsvに関して動作保証されている要件  
入力形式については [入出力データ仕様](docs/data_in_out.md) を参照 
## csv要件
* 行数5千万以下
* ID列と属性列はそれぞれ英数字及びバーティカルライン（|）から構成される空でない長さ64以下の文字列．  
* ID列と属性列はカンマ（,）で区切り，間や末尾にスペースを入れない．  
* 異なる行で共通のIDを持つものがあってはならない．  
* 属性の種類数は100以下  
ただし属性列が２列以上の場合，複数の属性の掛け合わせを一つの属性と見なして数える  
例として以下のようなcsvの場合，属性の種類数は`(a,X),(a,Y),(b,X),(b,Y),(c,Z)`の5つである
```csv
key_0,a,X
key_1,a,X
key_2,a,Y
key_3,a,Y
key_4,b,X
key_5,b,Y
key_6,c,Z
```

## 動作保証に用いたデータについて
[input_gen.py](./input_gen.py) を実行することで生成される input_a.csv と input_b.csv で動作保証を行っている．  
生成には10分程度かかる場合がある．  
### input_{a|b}.csv の概略

* 5千万行
* ID,属性はそれぞれランダムに生成された英数字及びバーティカルライン（|）からなる長さ64の文字列
* 属性の種類数は100通りずつ
* 二つのcsvのマッチング率は約6割（29995424件）

二つのデータの先頭を五行はそれぞれ以下である．  
`input_a.csv`
```
irBGkRk3qmqGaSFsxrNctK6joBBsda4hBEvVPoKrfcit9a8TU37hv|UDYHbbPvw1,SF6tjPH8omU1Lvnkdj5LeWeZjcbMDTtRA3OxjreBnRk51kjSGcOkZUZ9DsfXvnDS
4DJGiEDV51WZXVZy90XqCHimgByZSiNO134aV8eWGUQp63MeZfo0oCB5lqeIwPay,NsvgKWUlvtsMKXG1rJpM9x5pV4klKLCtCExBCi2y7TFFWDAklOSli1PBwkH86CiK
L9861zQ2gINgjdXDcgY0QSqi6HsjrxYxgBSZMSrreuanhZCthzQs8HsP89FIiPFe,9r99KyI8soTPUUrDByxJSmOHM6ZjWzsa|DaRvAvjuiiVjMkxgGKUgYw3fNkvju8Q
x7Wdjpyp9N7BOCLvwRI6ylBkvttJs0wA2wKCM8wJfAfYuRRfyuwRKvVkvmYs8IDt,VkGc0oNRPSX9n0MAxRXnG6XZzUGz|9mxo2k1XKLS7vcPmj37qGafZ7T9SigcZy2b
D3doUvq72fVnBNWw03eihgyajlhIlYYCyTN7o3FMCWrOyn9dfI5uNScl1b1DAUE4,ZMFkH8ffEE0skh53Ij4B1H0wcwcuQdRsoYU26Jwq40CVAKnuYKyiedjfM9bW212m
```
`input_b.csv`
```
lz9|yTpUTZN|uGPCBNpnEenik5lWRuUpvXBcuwMwc|WypA9CZAuzxWF1gnDpmkxb,C2laR|y5I3FAIEgb9eM7HBAxDC2JII8dsJld6G5fty6labpva3IHLROuq1j6gE8U
ROxRKTOxZ3IP6wv4z1CO2Y67506y812yDCZsbCFsxqyyzUoc1iAIyUtEb6aFKKAv,V8X1LBnLTFMm7l6uNH|gKxLmM3D1TZuNdljsgW5zNWr2i40QJuJqbIQdx4u9wCeW
QpTqJheeXmgCFmciSPxxVGUWjkdMFNB67qCTlHmI6VrU5FFZABXuNSaqfVRkbaTa,iV8R4Lp7Gj4iLO5RL6JSYPvpjXjveqApWB6Lpnkp5dt5Wbuz2epctu0R|SKGwuqF
K1MPkn8rNhFEnzqdwAYqT6B15n|m9WrcV0PaaPxXsaIw83zwTOXrifDqEZsb1AVi,WStLvc0fs0Ahkek|HPdz|GRTKQzLhviGG7dt4kVhzL32NXXz6bKI8D0bRQL4FZCF
|9|ZIz9rE5dd1qMa5u8YvkwgMU59oyJhPyyX6aBQRihcuPb1j39v6vby9njSlINF,DPOcgV0KIpjyYyT0ajteVAd|IpqLwRoMQMvVfaj7aycxV9Eq5Qm97i5gC8LqDWgg
```
