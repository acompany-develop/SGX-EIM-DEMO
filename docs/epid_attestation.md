# EPID Attestationの利用登録
    
> You may not disclose, distribute or transfer any part of the Materials, Software or Services except as provided in this Terms, and You agree to prevent unauthorized copying of the Materials, Software and Services.
> 

とのことなので，各々で利用登録をお願いします．

# 登録手順

1. [Intelのサイト](https://api.portal.trustedservices.intel.com/)に飛ぶ
2. アカウントを作成してsign inする
    - 参考
        
        右上
        ![Alt](/docs/image1.png)
        
        ![Alt text](/docs/image2.png)

        ![Alt text](/docs/image3.png)
        
3. Attestation Serviceのページへ移動する
    - 参考
        
        ![Alt text](/docs/image4.png)
        
4. Development AccessでSubscribeする(linkableとunlinkableはどちらでも良いらしい？)
    - 参考
        
        ![Alt text](/docs/image5.png)
        
5. 各種情報を確認する
    - 参考
        
        右上
        
        ![Alt text](/docs/image6.png)

        ![Alt text](/docs/image7.png)
        
6. clientのsettings.ini(client側の設定ファイル)の下記項目を修正する

```ini
SPID =
LINKABLE = 
IAS_PRIMARY_SUBSCRIPTION_KEY = 
IAS_SECONDARY_SUBSCRIPTION_KEY =
```
