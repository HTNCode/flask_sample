from flask import Flask

# インスタンスの生成
app = Flask(__name__)

# ROUTING
@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


# 実行
if __name__ == "__main__":
    app.run(debug=True)