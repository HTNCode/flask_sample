from flask import Flask, g, request

app = Flask(__name__)

@app.before_request # before_requestデコレータを使ってリクエストが来た時に実行される関数を定義
def before_request():
    g.user = get_user()

@app.route("/")
def do_hello():
    user = g.user # g変数を使ってユーザー情報を取得
    return f"こんにちは{user}さん"

@app.route("/morning")
def do_morning():
    user = g.user
    return f"おはようございます{user}さん"

@app.route("/evening")
def do_evening():
    user = g.user
    return f"こんばんは{user}さん"

# ユーザー情報を取得する関数
def get_user():
    user_info = {
        "name": "G太郎",
        "age": 20,
        "email": "g.tarou@example.com"
    }
    return user_info

if __name__ == "__main__":
    app.run(debug=True)