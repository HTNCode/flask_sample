import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ==================================================
# インスタンス生成
# ==================================================
app = Flask(__name__)

# ==================================================
# Flaskに対する設定
# ==================================================
# 乱数を設定
app.config["SECRET_KEY"] = os.urandom(24)
# DBファイルの設定
base_dir = os.path.dirname(__file__)
database = "sqlite:///" + os.path.join(base_dir, "data.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database # ここで設定したURIがDBの接続先になる
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # SQLAlchemyが不必要なトラッキングをしないように。推奨はFalse。大量のオーバーヘッドを引き起こしパフォーマンスに影響を与える可能性があるため。
db = SQLAlchemy(app) # これでdb変数を使用してSQLAlchemyを操作できるようにする

# ==================================================
# モデル
# ==================================================
# 課題
class Task(db.Model):
    # テーブル名
    __tablename__ = "tasks"
    
    # 課題ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 内容
    content = db.Column(db.String(200), nullable=False)
    
    # 表示用関数
    def __str__(self):
        return f"課題ID:{self.id}, 内容:{self.content}"

# ==================================================
# DB作成
# ==================================================
def init_db():
    with app.app_context():
        print("(1)テーブルを削除してから作成")
        db.drop_all()
        db.create_all()
        
        # データ作成
        print("(2)データ登録：実行")
        task01 = Task(content="課題01")
        task02 = Task(content="課題02")
        task03 = Task(content="課題03")
        db.session.add_all([task01, task02, task03])
        db.session.commit()
    
# ==================================================
# CRUD処理
# ==================================================
# 登録
def insert_task():
    with app.app_context():
        print("===========1件登録===========")
        task04 = Task(content="請求書作成")
        db.session.add(task04)
        db.session.commit()
        print("登録 =>", task04)

# 参照（全件）
def select_all():
    print("===========全件取得===========")
    with app.app_context():
        tasks = Task.query.all()
        for task in tasks:
            print(task)
        

# 参照（1件）
def select_one(pk):
    print("===========1件取得===========")
    with app.app_context():
        target = Task.query.filter_by(id=pk).first()
        print("更新後 =>", target)

# 更新
def update_task(pk):
    print("===========1件更新===========")
    with app.app_context():
        target = Task.query.filter_by(id=pk).first()
        target.content = "課題を変更"
        db.session.add(target)
        db.session.commit()

# 削除
def delete(pk):
    print("===========1件削除===========")
    with app.app_context():
        target = Task.query.filter_by(id=pk).first()
        db.session.delete(target)
        db.session.commit()
        print("削除 =>", target)

# ==================================================
# 実行
# ==================================================
if __name__ == "__main__":
    init_db() # DB初期化
    insert_task() #1件登録処理
    update_task(1) # 更新処理
    select_one(1) # 1件取得（更新後のデータを取得）
    delete(2) # 削除処理
    select_all() # 全件取得
        