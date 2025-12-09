import requests
import json
import sys # 新しくインポート

# サーバーのURLとエンドポイント
server_url = "http://localhost:5001/predict"

# テスト画像ファイルのパス
image_file_path = 'test_image.jpg' 

print(f"--- 接続テスト開始: {server_url} ---")

try:
    # ファイルを開く
    with open(image_file_path, 'rb') as f:
        print(f"ℹ️ ファイル {image_file_path} の読み込みに成功しました。") # ★この行が追加されていることを確認
        
        # リクエストの送信
        resp = requests.post(
            server_url, 
            files={"file": f}, 
            timeout=10
        )

    # 3. レスポンスの確認
    if resp.status_code == 200:
        print("✅ APIレスポンス (200 OK):")
        print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
    
    else:
        # ステータスコードが200以外の場合
        print(f"❌ エラーが発生しました: ステータスコード {resp.status_code}")
        print("-" * 20)
        print("サーバーレスポンス本文 (resp.text):")
        # サーバーから返されたエラーメッセージをそのまま表示
        print(resp.text) 
        print("-" * 20)

except FileNotFoundError:
    print(f"❌ ファイルエラー: テスト画像ファイル '{image_file_path}' が見つかりません。", file=sys.stderr)
except requests.exceptions.ConnectionError as e:
    print("❌ 接続エラー: Flaskサーバーが起動しているか、URLが正しいか確認してください。", file=sys.stderr)
    print(f"詳細: {e}", file=sys.stderr)
except requests.exceptions.RequestException as e:
    print(f"❌ リクエストエラー (その他の問題): {e}", file=sys.stderr)
except Exception as e:
    print(f"❌ 予期せぬエラー: {e}", file=sys.stderr)

print("--- テスト終了 ---")