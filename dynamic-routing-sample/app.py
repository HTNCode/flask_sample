from flask import Flask

app = Flask(__name__)

# ルーティング

# コンバーターなし
@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

# コンバーターあり
@app.route("/user/<username>")
def show_user_profile(username):
    return f"User: {username}"

# コンバーターあり（int）
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post: {post_id}"

# コンバーターあり（float）
@app.route("/weight/<float:weight>")
def show_weight(weight):
    return f"Weight: {weight}"

# 実行
if __name__ == "__main__":
    app.run(debug=True)
    