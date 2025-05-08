# ハッカソン作業用リポジトリ
* backend：バックエンド資源です。処理ひな型を置いているので、担当箇所を適宜修正してください。
* frontend：フロントエンド資源です。ほぼ何も入っていないのでご自由に変更してください。


# 開発環境構築（バックエンド向け）
1. GitHubからリポジトリをクローン
```
git clone https://github.com/MymtAggw2208/chatbot-hackathon.git
```

2. クローンしたディレクトリに移動
```
cd chatbot-hackathon
```

3. 仮想環境を作成
```
python -m venv .venv
```

4. 仮想環境を有効化 (各自のOSに合わせてコマンドを選択)
 macOS / Linux の場合
```
source .venv/bin/activate
```
 Windows の場合 (コマンドプロンプト)
```
.venv\Scripts\activate.bat
```
 Windows の場合 (PowerShell)
```
.venv\Scripts\Activate.ps1
```

5. 依存ライブラリをインストール
 requirements.txt を元に行います
```
pip install -r requirements.txt
```

6. (任意) .env ファイルの作成
環境変数を使う場合は、.env.example などを参考に .env ファイルをローカルに作成します（これはGit管理されない）<br>
現時点でGEMINIのAPIキーのみ指定しています

## ローカル起動手順
1. 仮想環境有効化<br>
   開発環境構築手順の「仮想環境を有効化」参照

2. backendに移動
```
cd backend
# requirements.txtに変更がある場合はinstallを実行
pip install -r requirements.txt
# 履歴テーブル作成時は以下を実行
# python create_table.py
```
3. アプリケーション起動
```
uvicorn app.main:app --reload
# ポート指定する場合
uvicorn app.main:app --reload --port 8001
```

4. ブラウザで確認
```
# ポート番号は適宜変更してください
http://localhost:8000/docs
```
