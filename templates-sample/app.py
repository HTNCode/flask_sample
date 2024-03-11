from flask import Flask, render_template

app = Flask(__name__)

# ルーティング

# TOPページ
@app.route("/")
def index():
    return render_template("index.jinja2")

# ユーザーページ
@app.route("/user/", defaults={'username': "ゲスト"})
@app.route("/user/<username>")
def user(username):
    return render_template("user.jinja2", username=username)

# ポストページ
@app.route("/post/", defaults={'post_id': 1})
@app.route("/post/<int:post_id>")
def post(post_id):
    return render_template("post.jinja2", post_id=post_id)

# 実行
if __name__ == "__main__":
    app.run(debug=True)


