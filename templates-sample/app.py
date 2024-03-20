from flask import Flask, render_template, abort

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
    return render_template("post.jinja2", show_id=post_id)

# render_templateで複数の値を渡す
@app.route("/multi/")
def multi():
    word1 = "テンプレートエンジン"
    word2 = "神社"
    return render_template("jinja/show1.jinja2", temp = word1, jinja = word2)

# 辞書型で値を渡す
@app.route("/dict/")
def dict():
    dict = {"temp": "テンプレートエンジン", "jinja": "神社"}
    return render_template("jinja/show2.jinja2", key = dict)

# リストで値を渡す
@app.route("/list/")
def list():
    hero_list = ["太郎", "次郎", "三郎"]
    return render_template("jinja/show3.jinja2", users = hero_list)

# クラスで値を渡す
class Hero:
    # コンストラクタ（初期化メソッド）
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    # 表示用関数
    def show(self):
        return f"名前：{self.name} 年齢：{self.age}"
    
    # __str__メソッドをオーバーライド（これをしないとオブジェクトが文字列として表示されない）
    def __str__(self):
        return self.show()
    
@app.route("/class/")
def show_jinja_class():
    taro = Hero("太郎", 20)
    return render_template("jinja/show4.jinja2", user = taro)

#　▼▼▼　ここから【制御文】　▼▼▼
# 「商品」クラス
class Item:
    # コンストラクタ（初期化メソッド）
    def __init__(self, id, name):
        self.id = id
        self.name = name
    # 表示用関数
    def __str__(self):
        return f"商品ID:{self.id} 商品名：{self.name}"
    
# 繰り返し処理
@app.route("/for_list/")
def show_for_list():
    item_list = [Item(1, "りんご"), Item(2, "みかん"), Item(3, "バナナ")]
    return render_template("for_list.html", items = item_list)

# 条件分岐
@app.route("/if_detail/<int:id>")
def show_if_detail(id):
    item_list = [Item(1, "りんご"), Item(2, "みかん"), Item(3, "バナナ")]
    return render_template("if_detail.html", show_id=id, items=item_list)

# 条件分岐2（ルーティングを重ねてtargetを受け取り、if elseで条件分岐）
@app.route("/if_else/")
@app.route("/if_else/<target>")
# target="colorless"をデフォルト値に設定
def show_jinja_if(target="colorless"):
    print(target)
    return render_template("if_else.html", color=target)

# フィルター
@app.route("/filter/")
def show_filter_block():
    word = "pen"
    return render_template("filter/block.html", show_word=word)

# フィルター（変数）
@app.route("/filter_var/")
def show_filter_variable():
    # クラスを作成
    momo = Hero("桃太郎", 20)
    kinta = Hero("金太郎", 25)
    ura = Hero("浦島太郎", 30)
    kagu = Hero("かぐや姫", 35)
    kasa = Hero("かさ地蔵", 40)    
    # リストに格納
    hero_list = [momo, kinta, ura, kagu, kasa]
    return render_template("filter/filter_list.html", heroes = hero_list)

# カスタム（自作）フィルターは以下のようにする
@app.template_filter("custom_filter")
def custom_filter(value, length=10):
    if len(value) > length:
        return value[:length] + "..."
    else:
        return value

# カスタム（自作）フィルターを使う
@app.route("/custom_filter/")
def show_custom_filter():
    word = "カスタムフィルターを使ってみる"
    return render_template("filter/custom_filter.html", show_word=word, show_word2=word)

# エラーハンドリングのモジュールのインポート
from werkzeug.exceptions import NotFound

# エラーハンドリング
@app.errorhandler(NotFound)
def show_404_page(error):
    msg = error.description
    print("エラー内容：", msg) # ステータスコード別のエラー内容を確認したい場合は、NotFoundをCtrl+クリックして確認できる
    return render_template("errors/404.html"), 404

# abort関数を使って例外を発生させる（これによって、明示的に404エラーを発生させ、その際に表示するメッセージ【error.description】を指定できる）
@app.route("/abort/")
def create_exception():
    abort(404, "要求されたページやファイルが見つかりません")



# 実行
if __name__ == "__main__":
    app.run(debug=True)


