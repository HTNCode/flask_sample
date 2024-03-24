from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
import os
#乱数を設定
app.config["SECRET_KEY"] = os.urandom(32)

# ROUTING
from forms import InputForm

# 入力画面
@app.route("/", methods=["GET", "POST"])
def input():
    form = InputForm()
    # POSTメソッドでリクエストがあった場合
    if form.validate_on_submit():
        session["name"] = form.name.data # Flaskのsessionオブジェクト【辞書】に値を設定
        session["email"] = form.email.data 
        return redirect(url_for("output")) # Flaskのredirect関数を使用し、その引数にurl_for関数を使用して302リダイレクトのリダイレクト先URLを生成、302リダイレクトする
    # GETメソッドでリクエストがあった場合（Flaskのsessionオブジェクト【辞書】に値がある場合はそこから値を取得し、フォームに設定）
    if "name" in session:
        form.name.data = session["name"]
    if "email" in session:
        form.email.data = session["email"]
    # GETリクエストの場合、またはPOSTリクエストでバリデーションエラーがあった場合
    return render_template("input.html", form=form)

# 出力画面（リダイレクト先のURLにアクセスされた場合の処理）
@app.route("/output")
def output():
    return render_template("output.html")


if __name__ == "__main__":
    app.run(debug=True)
    

# 補足：PRGパターンについて
# PRGパターンとは、Post/Redirect/Getパターンの略で、postリクエストに対してredirectを行ってgetリクエストを行うことで、遷移先の画面を表示するデザインパターン。
# このパターンを使用することで、ブラウザのリロードボタンを押してもPOSTリクエストが再送信される=formの二重送信を防ぐことができる。
# 特にSQLなどの処理を行う場合には、二重送信によってデータが重複して登録されたりすることを防ぐために使用されることが多い。
