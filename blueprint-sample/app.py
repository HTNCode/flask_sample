from flask import Flask, render_template

app = Flask(__name__)

# ========================
# Blueprintの登録（これにより、URLのパスが決まり、applicationディレクトリのビュー関数がそれぞれ呼び出される）
# ========================
from application.one.views import one_bp
app.register_blueprint(one_bp)

from application.two.views import two_bp
app.register_blueprint(two_bp)


@app.route('/')
def show_home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
