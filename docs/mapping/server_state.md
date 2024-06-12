Serverの`/info`APIを叩いた時に表示される`server_state`について

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
	"version": "v1.3.5"
}
```

`server_state`はclient0,1それぞれについてServerの進行度合いを`status_code`と`message`で表します．
`status_code`はエラー時の-1を除き，状態が進むほど大きくなります．

| status_code | message | 備考 |
| ---- | ---- | ---- |
| 0 | Initialized | 初期状態です． |
| 1 | Doing RA (1/3) | RA(RemoteAttestation)を開始した状態です． |
| 2 | Doing RA (2/3) | ClientからQuoteの取得を行う状態です． |
| 3 | Doing RA (3/3) | RAの結果をClientに返す状態です． |
| 4 | Matching | マッチング中の状態です． |
| 5 | Post-processing | マッチング後の後処理を行う状態です． |
| 6 | Waiting get-result | Clientからマッチング結果取得のリクエストが来るのを待っている状態です． |
| -1 | Handling error | エラー処理を行っている状態です．自動で初期状態に戻ります． |