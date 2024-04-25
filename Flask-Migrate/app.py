import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ==================================================
# インスタンス生成
# ==================================================
app = Flask(__name__)

# ==================================================
# Flaskに対する設定
# ==================================================
# 乱数を設定
app.config["SECRET_KEY"] = os.urandom(24)
base_dir = os.path.dirname(__file__)
database = "sqlite:///" + os.path.join(base_dir, "data.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ==================================================
# SQLAlchemy
# ==================================================
db = SQLAlchemy(app)
# flask_migrateを使用するための設定
Migrate(app, db)

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
# メモ
# ==================================================
# Flask-Migrateは、Flask-SQLAlchemyを使用している場合に、DBのマイグレーションを行うためのライブラリ。
# 主要なコマンドは以下の通り。
# - flask db init: マイグレーション用のディレクトリとファイルを作成
# - flask db migrate: マイグレーションスクリプトを作成するために使用され、現在のデータベースの状態とモデルの状態を記録するために使用
# - flask db upgrade: マイグレーションスクリプトをデータベースに適用するために使用。マイグレーションスクリプトを使用して、データベーススキーマを最新バージョンに更新する
# - flask db downgrade: マイグレーションスクリプトをデータベースから削除するために使用。マイグレーションスクリプトを使用して、データベーススキーマを以前のバージョンに戻す

# flask db initを実行すると、migrationsというディレクトリが作成される。
# migrationsディレクトリ：マイグレーションスクリプトが保存されるディレクトリ
# migrations/versionsディレクトリ：マイグレーションスクリプトが保存されるディレクトリ

# flask db migrate -m "コメント"を実行すると、migrations/versionsディレクトリにマイ具レーションスクリプトが作成される。
# 作成されるスクリプトファイル名は「revision番号（タイムスタンプ）」+「コメント」+「.py」になる
# ==================================================

# ==================================================
# CRUD操作
# ==================================================
# 登録

