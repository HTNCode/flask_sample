import os
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ==================
# DBファイル作成
# ==================
base_dir = os.path.dirname(__file__) # 現在のスクリプトがあるディレクトリのパスを取得
database = "sqlite:///" + os.path.join(base_dir, "data.sqlite") # data.sqliteという名前のデータベースを作成。"sqlite:///"はSQLiteを使用するための接頭辞。他にも"mysql://", "postgresql://"などがある
# データベースエンジンを作成
db_engine = create_engine(database, echo=True) # DBに接続するためのデータベースエンジン（DBMSがデータベースからデータをCRUDするための基盤）を作成。echo=Trueで実行するSQLをターミナルに表示できる
Base = declarative_base() # 型オブジェクトを継承したクラスを作成。このクラスを継承したクラスはテーブルとして扱うことができる

# ==================
# モデル（ORMの一つであるSQLAlchemyではデータベースのテーブルを表現するモデルクラスを定義する。そのためBaseと呼ばれる型オブジェクトを継承したクラスを作成する。モデルクラスはアプリ内でデータを表現するためのものでORMを通じてデータベースとやり取りする）
# ==================
class Item(Base):
    # テーブル名
    __tablename__ = "items" # テーブル名をitemsに設定
    # 商品ID
    id = Column(Integer, primary_key=True, autoincrement=True) # 商品IDを表すカラムを作成。primary_key=Trueで主キーに設定。autoincrement=Trueで自動採番する
    # 商品名
    name = Column(String(255), nullable=False, unique=True) # 商品名を表すカラムを作成。String(255)で文字列の長さを255文字に制限。nullable=FalseでNULLを許容しない。unique=Trueで一意制約を設定
    # 価格
    price = Column(Integer, nullable=False) # 価格を表すカラムを作成。nullable=FalseでNULLを許容しない
    
    #コンストラクタ
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    # 表示用関数
    def __str__(self):
        return f"Item(商品ID:{self.id}, 商品名:{self.name}, 価格:{self.price})"

# ==================
# テーブル操作
# ==================
print("(1)テーブル作成")
Base.metadata.create_all(db_engine) # モデルクラスを継承したクラスをテーブルとして作成

# セッション作成
session_maker = sessionmaker(bind=db_engine) # セッションを管理するためのセッションメーカーを作成
session = session_maker() # セッションオブジェクトを生成

print("(2)データ削除:実行")
session.query(Item).delete() # Itemモデルから全てのデータを削除
session.commit() # 削除したデータをコミットしてデータベースに反映

# データ作成
print("(3)データ登録:実行")
item01 = Item("団子", 100)
item02 = Item("肉まん", 150)
item03 = Item("どら焼き", 200)
session.add_all([item01, item02, item03]) # 複数のオブジェクトを一度にセッションに追加
session.commit()

print("(4)データ参照:実行")
item_all_list = session.query(Item).order_by(Item.id).all() # Itemモデルから全てのデータを取得し、商品IDで昇順に並べ替えする（クエリが使える）
for row in item_all_list:
    print(row)

print("(5)データ更新1件:実行")
target_item = session.query(Item).filter(Item.id == 1).first() # 商品IDが1のデータを取得（クエリが使える）
target_item.price = 500
session.commit()
target_item = session.query(Item).filter(Item.id == 3).first() # 商品IDが3のデータを取得（クエリが使える）
print("確認用", target_item)

print("(6)データ更新複数件:実行")
target_item_list = session.query(Item).filter(or_(Item.id==1, Item.id==2)).all() # 商品IDが1または2のデータを取得（or_()はまたは）（クエリが使える）
for target_item in target_item_list:
    target_item.price =999
session.commit()
item_all_list = session.query(Item).order_by(Item.id).all() # Itemモデルから全てのデータを取得し、商品IDで昇順に並べ替え（クエリが使える）
print("確認")
for row in item_all_list:
    print(row)