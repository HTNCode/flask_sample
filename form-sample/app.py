from flask import Flask, request

app = Flask(__name__)

# GETでデータ取得(クエリパラメータ「?name=XXX」を付与してアクセスするとその値を取得して表示する)
@app.route("/get")
def do_get():
    name = request.args.get('name')
    return f"Hello, {name}!"

# POSTでデータ取得
@app.route("/", methods=["GET","POST"])
def do_get_post():
    if request.method == "POST":
        name = request.form.get("name") # フォームからnameを取得
        return f"こんにちは, {name}!"
    return """
        <h2>
        <form method="post">
            名前:<input type="text" name="name"> <!-- フォームのnameを上記のrequest.form.get("name")で取得 -->
            <input type="submit" value="送信">
        </form>
    """
    

if __name__ == "__main__":
    app.run(debug=True)