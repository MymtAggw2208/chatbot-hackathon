# ハッカソン作業用リポジトリ
* backend：バックエンド資源です。処理ひな型を置いているので、担当箇所を適宜修正してください。
* frontend：フロントエンド資源です。ほぼ何も入っていないのでご自由に変更してください。


# 開発環境構築（バックエンド向け）
## GitHubからリポジトリをクローン
```
git clone https://github.com/MymtAggw2208/chatbot-hackathon.git
```

## クローンしたディレクトリに移動
```
cd chatbot-hackathon
```

## 仮想環境を作成
```
python -m venv .venv
```

## 仮想環境を有効化 (各自のOSに合わせてコマンドを選択)
### macOS / Linux の場合
```
source .venv/bin/activate
```
### Windows の場合 (コマンドプロンプト)
```
.venv\Scripts\activate.bat
```
### Windows の場合 (PowerShell)
```
.venv\Scripts\Activate.ps1
```

## 依存ライブラリをインストール
### requirements.txt を元に行います
```
pip install -r requirements.txt
```

## (任意) .env ファイルの作成
環境変数を使う場合は、.env.example などを参考に .env ファイルをローカルに作成します（これはGit管理されない）
