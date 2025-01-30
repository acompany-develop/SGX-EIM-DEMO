# SGX-EIM-DEMO
# 用語

| 用語 | 説明 |
| --- | --- |
| ISV | SGXに関するリクエストを受け付けるServer |
| Firm | ISVに対してリクエストを送るClient |
| RA | Remote Attestation，SGXが安全であることを示すためのプロトコル |
| MAA | Microsoft Azure Attestation，SGXが安全であることを示すためのプロトコル |

ISVやFirmはそれぞれServerやClientと記載することもある．
# ディレクトリ概要
```
.
├── README.md
├── demo_docker/
├── docs/
|   └── cross_table/
└── licenses　　　　　　　　　　　　　
    └── LICENSE_linux-sgx
```
- [demo_docker/](./demo_docker/README.md): dockerを用いたdemo用コード
- [docs/cross_table/](./docs/cross_table/README.md): `cross_table`バイナリについてのドキュメント
- [licenses/LICENSE_linux-sgx](./licenses/LICENSE_linux-sgx): 配布バイナリで利用しているライセンス


# 動作確認済み条件

- OS
    - Ubuntu22.04
- CPU
    - 以下動作確認済み
        - Intel(R) Xeon(R) E-2288G CPU @ 3.70GHz ([Azure Standard DC4s v2](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-computing-enclaves))
        - Intel(R) Xeon(R) E-2174G CPU @ 3.80GHz (IBM Cloud)
- メモリ
    - 64GB以上 ※1
