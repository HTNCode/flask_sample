import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# ==================================================
# DBファイル作成
# ==================================================
base_dir  = os.path.dirname(__file__)
database = "sqlite:///" + os.path.join(base_dir, "data.sqlite")
# データベースエンジンを作成
db_engine = create_engine(database, echo=True)
Base = declarative_base()

# ==================================================
# モデル
# ==================================================
# \商品
class Item(Base):
    # テーブル名
    __tablename__ = "items"
    # 商品ID
    item_id = Column(Integer, primary_key=True)
    # 商品名
    item_name = Column(String, nullable=False, unique=True)
    # 価格
    price = Column(Integer, nullable=False)
    # リレーション（secondaryで多対多のリレーションを表現し、中間テーブルとして使用されるテーブルを指定。ここではItemモデルとShopモデルの間にStockモデルを挟んで多対多のリレーションを表現している）
    shops = relationship("Shop", secondary="stocks", back_populates="items") 

# 店舗
class Shop(Base):
    # テーブル名
    __tablename__ = "shops"
    # 店舗ID
    shop_id = Column(Integer, primary_key=True)
    # 店舗名
    shop_name = Column(String(255), nullable=False, unique=True)
    # リレーション
    items = relationship("Item", secondary="stocks", back_populates="shops")

# 在庫
class Stock(Base):
    # テーブル名
    __tablename__ = "stocks"
    # 店舗ID
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), primary_key=True)
    # 商品ID
    item_id = Column(Integer, ForeignKey("items.item_id"), primary_key=True)
    # 在庫
    stock = Column(Integer)
print("(1)テーブルを削除してから作成")
Base.metadata.drop_all(db_engine)
Base.metadata.create_all(db_engine)

# セッションの生成
session_maker = sessionmaker(bind=db_engine)
session = session_maker()

# 店舗データの追加
new_shop = Shop(shop_id=1, shop_name="テスト店舗")
session.add(new_shop)
session.commit()

# 商品データの追加
new_item = Item(item_id=1, item_name="テスト商品", price=100)
session.add(new_item)
session.commit()

# 在庫データの追加
new_stock = Stock(shop_id=1, item_id=1, stock=10)
session.add(new_stock)
session.commit()

print("(3)データ参照：実行")
print("■：Shopの参照")
target_shop = session.query(Shop).filter_by(shop_id=1).first() # 店舗IDが1の店舗情報を取得
print(f"店舗名：{target_shop.shop_name}")
print("■：リレーションから商品の参照")
# target_shopが持つ商品情報を取得する
for item in target_shop.items:
    # itemに対応する在庫情報を取得する
    stock = session.query(Stock).filter_by(shop_id=target_shop.shop_id, item_id=item.item_id).first()
    # 在庫数を表示する
    print(f"商品名：{item.item_name} -> 在庫数：{stock.stock}")