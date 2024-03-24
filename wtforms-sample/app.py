from flask import Flask, render_template, request

app = Flask(__name__)

from forms import UserInfoForm # forms.pyからUserInfoFormをインポート

# ユーザー情報入力画面
@app.route("/", methods=["GET", "POST"])
def show_enter():
    # フォームの作成
    form = UserInfoForm(request.form)
    # POSTメソッドでリクエストがあった場合
    if request.method == "POST" and form.validate():
        return render_template("result.html", form=form) # テンプレートファイルを指定し、作成したフォームを渡す
    # POSTメソッド以外でリクエストがあった場合もしくはform.validate()がFalseの場合
    return render_template("enter2.html", form=form) # テンプレートファイルを指定し、作成したフォームを渡す

if __name__ == "__main__":
    app.run(debug=True)