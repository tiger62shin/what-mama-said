# 「Knowledge → GROWI 移行」プログラム

- 情報共有サービス Knowledge のデータ (記事) を GROWI に移行する
- GROWI アクセスクライアント
<br/><br/>

# DEMO
<br/><br/>

# Features
<br/><br/>

# Requirement

* Python 3.9.7
* requests 2.27.1
* psycopg2 2.9.3
<br/><br/>

# Installation
<br/><br/>

# Usage

## migration.py

Knowledge → GROWI 移行

```
usage: migration.py [-h] --kbdb_host KBDB_HOST [--kbdb_port KBDB_PORT] --kbdb_name KBDB_NAME --kbdb_user KBDB_USER --kbdb_passwd KBDB_PASSWD --growi_host GROWI_HOST
                    --growi_port GROWI_PORT [--growi_usessl] --growi_apikey GROWI_APIKEY --growi_user GROWI_USER

Knowledge to GROWI contents migration.

optional arguments:
  -h, --help            show this help message and exit
  --kbdb_host KBDB_HOST
                        Knowledge DataBase hostname.
  --kbdb_port KBDB_PORT
                        Knowledge DataBase port no.
  --kbdb_name KBDB_NAME
                        Knoeledge DataBase name.
  --kbdb_user KBDB_USER
                        Knowledge DataBase user name.
  --kbdb_passwd KBDB_PASSWD
                        Knowledge DataBase user password.
  --growi_host GROWI_HOST
                        GROWI host name.
  --growi_port GROWI_PORT
                        GROWI API port no.
  --growi_usessl        GROWI access with SSL.
  --growi_apikey GROWI_APIKEY
                        GROWI API key.
  --growi_user GROWI_USER
                        GROWI user name.
```

## GrowiClient

  GROWI アクセス クライアント

- create_page

  GROWI のベージを作製する

- set_attachment

  指定されたファイルを指定された GROWI ページの添付ファイルとして設定する

- update_page

  GROWI ページを更新する

- is_draft

  DRAFT ページに対する処理かどうかを返す

## GrowiPage

GROWI ページを表す

- replace_attachment

  本文の指定されたファイルの参照 (リンク) を指定された参照 (リンク) に置き換える

- initialize_attachments_info

  GROWI ページの添付ファイル情報を設定する

- add_attachment_info

  添付ファイル情報を追加する

- get_attachment_info

  この GROWI ページが指定されたファイル名の添付ファイル情報を返す

- remove_attachment_info

  この GROWI ページから指定された添付ファイル ID の添付ファイル情報を削除する

## GrowiAttachment:

  GROWI 添付ファイルを表す

## growiclient_sample.py

  GrowiClient クラスの使い方サンプル
<br/><br/>

# Note
<br/><br/>

# Author

* Shinji Miyahara
* Blog : https://tiger62shin.hatenablog.com/
<br/><br/>

# License

[MIT license](https://en.wikipedia.org/wiki/MIT_License).
