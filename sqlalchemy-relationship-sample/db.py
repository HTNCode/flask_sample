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
# 部署
class Department(Base):
    # テーブル名
    __tablename__ = "departments"
    # 部署ID
    id = Column(Integer, primary_key=True, autoincrement=True) # autoincrement=Trueで自動採番
    # 部署名
    name = Column(String, nullable=False, unique=True)
    # リレーション: 1対多
    employees = relationship("Employee", back_populates="department") # back_populatesで逆参照する。逆参照とは、EmployeeからDepartmentにアクセスすること
    # 表示用関数
    def __str__(self):
        return f"部署ID:{self.id}, 部署名:{self.name}"

# 従業員
class Employee(Base):
    # テーブル名
    __tablename__ = "employees"
    # 従業員ID
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 従業員名
    name = Column(String, nullable=False)
    # ForeignKeyには「テーブル名.カラム名」を指定（ForeignKeyは外部キー制約を表現するためのクラスで、テーブル間のリレーションシップを表現する時に使用される。あるテーブルの列が、他テーブルの特定列と関連付けられていることを保証する制約）
    department_id = Column(Integer, ForeignKey("departments.id")) 
    # リレーション: 1対1
    department = relationship("Department", back_populates="employees", uselist=False) # uselist=Falseで1対1の関係を表現
    # 表示用関数
    def __str__(self):
        return f"従業員ID:{self.id}, 従業員名:{self.name}"

# ==================================================
# テーブル操作
# ==================================================
print("(1)テーブルを削除してから作成")
Base.metadata.drop_all(db_engine)
Base.metadata.create_all(db_engine)

# セッションの生成
session_maker = sessionmaker(bind=db_engine)
session = session_maker()

# データ作成
print("(2)データ登録：実行")
# 部署
dept01 = Department(name="開発部")
dept02 = Department(name="営業部")

#従業員
emp01 = Employee(name="太郎")
emp02 = Employee(name="次郎")
emp03 = Employee(name="三郎")
emp04 = Employee(name="四郎")

# 部署に従業員を紐づける
# 開発部：太郎、次郎
# 営業部：三郎、四郎
dept01.employees.append(emp01)
dept01.employees.append(emp02)
dept02.employees.append(emp03)
dept02.employees.append(emp04)

# セッションで「部署」を登録
session.add_all([dept01, dept02])
session.commit()

print("(3)データ参照：実行")
print("■：Employeeの参照")
target_emp = session.query(Employee).filter_by(id=1).first() # filter_byは列名と値のペアで指定した条件に一致する行を取得する（一方でfileter()は条件式を指定する）
print(target_emp)
print("■：Employeeに紐づいたDepartmentの参照")
print(target_emp.department)

print("■：Departmentの参照")
target_dept = session.query(Department).filter_by(id=1).first()
print(target_dept)
print("■：Departmentに紐づいたEmployeeの参照")
for emp in target_dept.employees:
    print(emp)
    