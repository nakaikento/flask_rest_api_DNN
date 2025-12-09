import io
import json
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request, render_template, url_for
import os # ファイル操作のために os をインポート
from werkzeug.utils import secure_filename # ファイル名を安全にするためのモジュールをインポート

# 画像の保存先ディレクトリを設定
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # 許可する拡張子

# Flaskアプリケーションの初期化
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ImageNetのクラスインデックスファイルをロード
try:
    with open('imagenet_class_index.json') as f:
        imagenet_class_index = json.load(f)
except FileNotFoundError:
    print("Error: imagenet_class_index.jsonが見つかりません。プロジェクトフォルダにダウンロードしてください。")
    # ローカル実行時にはこのエラーで終了することが望ましい
    exit()

# モデルのロード (DenseNet121, 事前学習済み)
model = models.densenet121(pretrained=True)
model.eval()

def transform_image(image_bytes):
    # 画像の前処理定義
    my_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225]
        )
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

def get_prediction(image_bytes):
    # 画像のテンソル化
    tensor = transform_image(image_bytes=image_bytes)
    # 推論実行
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    
    # クラスIDとクラス名を取得して返す
    return imagenet_class_index[predicted_idx]

# 許可された拡張子かどうかをチェックするヘルパー関数
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# APIエンドポイントの定義
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # リクエストからファイルを取得
        file = request.files['file']
        img_bytes = file.read()
        
        try:
            class_id, class_name = get_prediction(image_bytes=img_bytes)
            # 推論結果をJSONで返す
            return jsonify({
                'class_id': class_id, 
                'class_name': class_name
            })
        except Exception as e:
            # 推論中のエラーを捕捉
            return jsonify({'error': f'推論中にエラーが発生しました: {str(e)}'}), 500

# @app.route('/', methods=['GET'])
# def index():
#     # サーバーが起動しているか確認するためのシンプルなルート
#     return jsonify({'status': 'ok', 'message': 'API is running'})


@app.route('/')
def upload_form():
    return render_template('index.html') # Flaskのrender_template関数を使用

# ファイルをアップロードし、予測を行うルート
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        
        # ファイルの存在と拡張子のチェック
        if not file or file.filename == '' or not allowed_file(file.filename):
            return render_template('index.html', error='有効な画像ファイルを選択してください (png, jpg, jpeg, gif)。')

        try:
            # 1. 画像ファイルを安全なファイル名で保存
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Flaskのio.BytesIOを使い、メモリから直接読み込むように修正していた場合は、
            # 一時的にファイルオブジェクトの位置を先頭に戻してから保存します。
            # 今回はファイル全体をメモリに読み込むため、seek(0)は不要ですが、念のため保存処理を追加。
            
            file.save(filepath)
            
            # 2. 予測処理のために、保存したファイルを再度開いてバイトを読み込む
            # file.save() を行うとファイルポインタが終端にあるため、
            # 予測関数には元のファイルの内容を再度渡す必要があります。
            with open(filepath, 'rb') as f:
                img_bytes = f.read()

            class_id, class_name = get_prediction(image_bytes=img_bytes)
            
            # 3. テンプレートに渡す画像のURLを作成
            # Flaskのurl_forを使って、静的ファイルへのパスを作成
            image_url = url_for('static', filename=filename)
            
            # 4. 結果と画像のURLを HTML テンプレートに渡してレンダリング
            return render_template('index.html', 
                                   result={
                                       'class_id': class_id, 
                                       'class_name': class_name
                                   },
                                   # 画像のURLをテンプレートに渡す
                                   uploaded_image_url=image_url,
                                   success=True)

        except Exception as e:
            return render_template('index.html', error=f'推論処理中にエラーが発生しました: {str(e)}')

# =======================================================
# 以下のブロックをファイルの最後に追加してください
# =======================================================
if __name__ == '__main__':
    # デバッグモードを有効にして起動（ログがより詳細になる）
    app.run(debug=True, port=5001)  # ポート番号を5001に変更