# 🚀 PyTorch Image Classification API with Flask (flask_rest_api_DNN)

このプロジェクトは、**PyTorch** の学習済みモデル（DenseNet121など）を使用した画像認識機能を、**Flask** を利用した REST API として公開するシステムです。

Web UI も組み込まれており、ブラウザから簡単に画像ファイルをアップロードし、推論結果を確認できます。


## 🛠️ 環境構築手順 (macOS / pyenv)

本プロジェクトは `pyenv` で管理された仮想環境内で動作確認を行っています。

### 1. 仮想環境の作成と有効化

```bash
# Python 3.10.12 バージョンを指定して仮想環境を作成
pyenv virtualenv 3.10.12 flask-api-env
```

#### 仮想環境を有効化
```bash
pyenv local flask-api-env
```

### 2. 依存ライブラリのインストール
以下の主要ライブラリをインストールします。特に NumPy のバージョンは PyTorch との互換性のため、1.x 系に固定しています。


#### 依存ライブラリを一括インストール
```bash
# NumPy のバージョンを 1.26.4 に固定
pip install Flask torch torchvision Pillow requests numpy==1.26.4
```

## ⚙️ サーバーの起動とポート設定
macOSではシステムプロセスがポート 5000 を占有する可能性があるため、本プロジェクトはポート 5001 で起動するように設定されています。

### 1. サーバーの起動
app.py ファイルの末尾で port=5001 が指定されていることを確認し、以下のコマンドでサーバーを起動します。

```bash
python app.py
```
ログに Running on http://127.0.0.1:5001 と表示されれば成功です。

### 2. ファイル構造
アップロードされた画像は、static フォルダに一時的に保存されます。

```bash
flask_rest_api_DNN/
├── app.py
├── client.py
├── templates/
│   └── index.html  # Web UI
└── static/         # アップロード画像や静的ファイルを格納
```

## 🧪 Web UI / API テスト方法
### 1. Web UI でのテスト (推奨)
ブラウザを開き、以下のURLにアクセスしてください。

[http://127.0.0.1:5001/](http://127.0.0.1:5001/)  

画面から画像を選択し、「アップロードして予測」ボタンを押すことで、モデルの推論結果とアップロード画像が表示されます。

### 2. API エンドポイント (プログラムからのテスト)
client.py スクリプトを使用して、API の動作をターミナルからテストできます。

```bash
python client.py
```
API エンドポイントは http://localhost:5001/upload です。

## 📘 参考資料
本プロジェクトのコアとなる API 実装は、以下の PyTorch チュートリアルを参考にしています。

[PyTorch チュートリアル (日本語訳): Deploying PyTorch with Flask on Heroku (Colab Notebook)](https://colab.research.google.com/github/YutaroOgawa/pytorch_tutorials_jp/blob/main/notebook/5_Deployment/5_1_flask_rest_api_tutorial_jp.ipynb#scrollTo=evb-QuFH-AHc)