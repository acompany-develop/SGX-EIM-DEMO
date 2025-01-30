# 入力形式

- カンマ(,)区切りのCSV
- 1行目にはheaderを記載
- 1列目にはマッチングで突合に用いるID列を記載
- 2列目以降には属性を記載

### 例
```csv
ID,height,weight
id1,170,70
id2,180,60
id3,170,60
```

入力ファイルの動作保証要件については[guarantee.md](guarantee.md)を参照  

# 出力形式
- カンマ(,)区切りのCSV
- 1行目にはheaderを記載
    - header の1列目はnumber_of_rowsを記載
    - 2列目以降には <client_bit>:<attribute> の形式で属性名を記載
- 2行目以降には集計結果を記載
    - 1列目にはその属性集合の個数を記載
    - 2列目以降には属性を記載
    - 集計数が閾値`k`未満の行は出力されない  
      閾値`k`はバイナリ実行時に引数で指定する

### 例
```csv
number_of_rows,0:height,0:weight,1:dominant
10,170,60,right
5,170,70,right
7,180,60,left
```

# 入出力例
### Client0の入力
```
ID,height,weight
id1,170,70
id2,180,60
id3,170,60
id4,170,70
id5,180,60
id6,180,60
id7,170,60
id8,180,60
id9,170,60
```

### Client1の入力
```
ID,dominant
id1,right
id2,right
id3,right
id4,left
id5,left
id6,right
id7,left
id8,left
id9,right
```

### 出力(`k=0`)
```
number_of_rows,0:height,0:weight,1:dominant
1,170,60,left
2,170,60,right
1,170,70,left
1,170,70,right
2,180,60,left
2,180,60,right
```
### 出力(`k=2`)
number_of_rowsが2未満の行が出力されない
```
number_of_rows,0:height,0:weight,1:dominant
2,170,60,right
2,180,60,left
2,180,60,right
```
