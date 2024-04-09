import os
import sqlite3

# ==================
# DBファイル作成
# ==================

base_dir = os.path.dirname(__file__) # 現在のスクリプトがあるディレクトリのパスを取得
database = os.path.join(base_dir, "data.sqlite") # data.sqliteという名前のデータベースを作成

# ==================
# SQL
# ==================
# 接続
conn = sqlite3.connect(database) # データベースに接続
print("▼▼▼▼▼▼▼▼▼ コネクションの接続 ▼▼▼▼▼▼▼▼▼")
print()
# カーソルを取得
cur = conn.cursor() 
# テーブル削除SQL
drop_sql = """
DROP TABLE IF EXISTS items;
"""
cur.execute(drop_sql) # executeはSQLを実行するメソッド。引数にSQL文を指定して実行
print("(1)対象テーブルがあれば削除")
# テーブル作成SQL
create_sql = """
CREATE TABLE items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name STRING UNIQUE NOT NULL,
    price INTEGER NOT NULL
)
"""
cur.execute(create_sql)
print("(2)テーブル作成")
# データ登録SQL
insert_sql = """
INSERT INTO items (item_name, price) VALUES(?, ?)
"""
insert_data_list = [
    ("みかん", 100), ("りんご", 200), ("ばなな", 100), ("おにぎり", 150)
]

cur.executemany(insert_sql, insert_data_list) # executemanyは複数のデータを一度に登録するメソッド。引数にSQL文とデータのリストを指定して実行
conn.commit() # commitでデータベースへの変更を確定する
print("(3)データ登録:実行")
# データ参照（全件）SQL
select_all_sql = """
    SELECT * FROM items
    """
cur.execute(select_all_sql)
print("(4)----------------全件取得:実行----------------")
data = cur.fetchall() # fetchallは全てのデータを取得するメソッド
print(data)
# データ参照(1件)SQL（?はプレースホルダといい、SQL文の実行時に値を変数のように埋め込める。SQLインジェクションなどの攻撃を防ぐことができる)  
select_one_sql = """
    SELECT * FROM items WHERE item_id = ?
    """
id = 3
cur.execute(select_one_sql,(id,))
print("(5)----------------1件取得:実行----------------")
data = cur.fetchone() # fetchoneは1件のデータを取得するメソッド
print(data)
# データ更新SQL
update_sql = """
    UPDATE items SET price = ? WHERE item_id = ?
    """
price = 500
id = 1
cur.execute(update_sql,(price,id)) # price, idの順番で指定
print("(6)----------------データ更新:実行----------------")
conn.commit()
cur.execute(select_one_sql,(id,)) #id,の,を入れるのはタプルとして認識させるため
data = cur.fetchone()
print("確認のため1権取得:実行",data)
# データ削除SQL
delete_sql = """
    DELETE FROM items WHERE item_id = ?
    """
id = 3
cur.execute(delete_sql,(id,))
conn.commit()
print("(7)----------------データ削除:実行----------------")
cur.execute(select_all_sql)
data = cur.fetchall()
print("確認のため全件取得:実行",data)
# 閉じる
conn.close() # closeしないとデータベースファイルがロックされたままになる
print()
print("▲▲▲▲▲▲▲▲▲ コネクションのクローズ ▲▲▲▲▲▲▲▲▲")