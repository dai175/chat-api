# chat-api

## 概要
これはチャットアプリケーションのサンプルAPIです。以下の機能が含まれています。
- 1対1のチャット
- 複数人のグループチャット
- メッセージの一覧取得、投稿、削除
- メッセージの未読、既読の確認
- 新着メッセージの通知
- 通知設定
  - Push通知
  - メール通知
  - 通知しない

## インストール方法
以下の手順でインストールできます。

```bash
# リポジトリをクローンします
git clone https://github.com/dai175/chat-api.git

# ディレクトリに移動します
cd chat-api

# 環境変数ファイルを作成し、必要に応じて更新します
cp .env.develop .env

# Dockerコンテナを起動します
docker compose up -d

# データベースをセットアップします
docker compose exec api python setup_db.py
```

## Push通知の設定
Push通知にPusherを利用しています。以下の手順で設定が必要です。
1. Pusherのアカウントを作成します。以下のURLにアクセスしてください。  
https://pusher.com/beams/
2. インスタンスを作成してください。
3. Overview画面からWebの通知設定を行ってください。
4. Key画面からInstance ID、Primary Keyを確認し、`.env`ファイルに以下の内容を追記してください。
    ```
    PUSHER_INSTANCE_ID=xxxxxx(Instance ID)
    PUSHER_SECRET_KEY=xxxxxx(Primary Key)
    ```

## 動作確認
1. ユーザーを作成します。以下のURLにアクセスし、`POST /register`から作成してください。  
http://localhost:8000/docs# 
2. ログイン画面からメールアドレスとパスワードを入力してログインします。以下のURLにアクセスしてください。  
http://localhost:8000
3. チャット画面からチャットを開始します。具体的な手順は以下の通りです。
   - グループチャット
      1. `Chat Type`から`Group Chat`を選択します。
      2. `Room ID`に部屋番号（任意の文字列）を入力します。
      3. `Connect`ボタンをクリックします。
      4. `Message`にメッセージを入力し、`Send`ボタンで送信します。
   - ダイレクトチャット
      1. `Chat Type`から`Direct Chat`を選択します。
      2. `Receiver ID`に相手のユーザーID（UUID）を入力します。
      3. `Connect`ボタンをクリックします。
      4. `Message`にメッセージを入力し、`Send`ボタンで送信します。
4. 開発用メールサーバーとしてMailHogを利用しています。メール通知を確認するには、以下のURLにアクセスしてください。  
http://localhost:8025

## その他
テストコードは未作成です。