<style>
r { color: Red }
o { color: Orange }
g { color: Green }
</style>

# 動作保証について
入力するcsvに関して動作保証されている要件
入力形式については [入出力データ仕様](docs/data_in_out.md) を参照 
## csv要件
* 行数5千万以下
* 利用可能文字は[graphical representation](https://en.cppreference.com/w/cpp/string/byte/isgraph)で定義されたもの．<r>ただし，`,`はID列と属性列の境界文字として解釈されるため、ID列に`,`は利用不可</r>．
```
digits (0123456789)
uppercase letters (ABCDEFGHIJKLMNOPQRSTUVWXYZ)
lowercase letters (abcdefghijklmnopqrstuvwxyz)
punctuation characters (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
```
* ID列と属性列は利用可能な文字から構成される長さ1以上64以下の文字列．

ただし，[入出力データ仕様](docs/data_in_out.md) に記載の通り，属性を`key,a,X`のように二つ以上入力した場合，内部では2個目以降の`,`を解釈せず`"a,X"`として扱われる．
* ID列と属性列はカンマ（,）で区切り，間や末尾にスペースを入れない．
* 異なる行で共通のIDを持つものがあってはならない．<r>そのため，ID列は必ずユニークにしておく必要がある．</r>
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
* ID,属性はそれぞれランダムに生成された，利用可能文字からなる長さ64の文字列
* 属性の種類数は100通りずつ
* 二つのcsvのマッチング率は約6割（29995424件）

二つのデータの先頭を五行はそれぞれ以下である．
`input_a.csv`
```
key_C_$XEA[pBBuF.8}:!u`(7uyC:J.rc<!LH^9"DUN*U~.`]9um6suCv8(BMrp',2Z#tL,.;xF,Y,I,LBd$C,$IY(Nhh,tSCb,-[Ud$[@t@,`nI8L!jrC)k,J*~f,H'o
key_]I0Wc~ur\YC.e51mCq.Xj^~nzB<HCqVp=L7{HyzK8KIa7E4&!W<a7RCC%:(O,xBx;4,k,?,,|YkI~92OJRaZ};,',$fXd[uxs,rS<D\R(#%"e},S,$_,er#o{vxkX
key_]H=b~41>t]j4cLH8>Quc\s$"#vuHr/+DyAamFk75!]7&T[k:l&7KK5tfj>2$,xBx;4,k,?,,|YkI~92OJRaZ};,',$fXd[uxs,rS<D\R(#%"e},S,$_,er#o{vxkX
key_M_kkO!uF-Wx0~:K/rfYm{";diSqA?e1I>4pYit'y=|Msv"+av9;3Y(7Bu*eE,v,%6,C9I,LrA12,+}fFY1,,G>,L,}BhBxcJc'lNHwN$G3U)ADCppq4G,*!MfH;S,
key_nkrdPn2l:C@_mQ?Sfn}r>-(&-<5fLjNJb71:7{}(FpCwA&[emj4=L6FF+)cW,|[,>e,opw;l.DN`BF,Mf,eWk7b,,,JTyvM6,kep-|v#x-U(bxu>,92psnRs,ku@q
```
`input_b.csv`
```
key_1T@{BK\]shmc%j)ltVP>9.cnV&r4wj/T8=gCaq^ECo)YVd6#R/o]2.9_Q3P$,#y\^,|R,8S90Ev,,dLYIyMs(,6jd87,vq*C,_$5,4X[E>_tduEFdH7B=Q0m,,Q|z
key_0P?xEG|/tGQ%;Xk:>1R3Zob~S3FAg1%8}SR[(LUD.hioXb_]MT!:MO67YCH),/T,,XJLah,|JJ8r,NEg,jT7G&#f*xo)I,sax^OC+-uj,jR;#3}7-i%Z,?,qR~\,4
key_/0~1U^;s:AKxwS+$*1Nwj]ihgZULS_>\5[2Y^KCu]^V%vc}Zp|Uu[7.eao%U,|wpJ)]R0~,,"21I9!,1oQcvnI,#,e,yH.msoKy)-|pV%^,@,,qoa*QU%b.9/>m',
key_}gq)^.gqEOC?8p#2{oW9E#Qf'^:fks^pI"0Erwb=QD|ok9P+Z`3hRlR2ov"C,Q\&<:}[,L_,9>,nl,Z3juv/,wFzk,Slk,\.14A<,w,-gPtJ1mq\GH*},Yu\]Vh:_
key_HE.Bx"zZGQBn_SXqXPSOnY7ssE0j=-1UL9'xzyU;<t[5V$`CCWv|wdvn~@'p,/T,,XJLah,|JJ8r,NEg,jT7G&#f*xo)I,sax^OC+-uj,jR;#3}7-i%Z,?,qR~\,4
```
