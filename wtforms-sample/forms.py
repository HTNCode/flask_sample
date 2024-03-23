from wtforms import Form
from wtforms.fields import (
    StringField, IntegerField, PasswordField, DateField, RadioField, SelectField, BooleanField, TextAreaField,EmailField, SubmitField
)

# 使用するvalidatorをインポート（wtformsではバリデーションを行うためのvalidatorが用意されている）
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Email

# ==============================
#Formクラス
# ==============================
# ユーザー情報クラス
class UserInfoForm(Form): # Formクラスをwtformsから継承
    # 名前：文字列入力
    name = StringField("名前: ", validators=[DataRequired("名前は必須入力です")], render_kw={"placeholder": "（例）山田太郎"}) # render_kwはHTMLの属性を指定するもの
    # 年齢：整数入力
    age = IntegerField("年齢: ", validators=[NumberRange(18, 100, "入力範囲は18歳から100歳です")], default=20) # defaultは初期値を指定するもの
    # パスワード：パスワード入力
    password = PasswordField("パスワード: ", validators=[Length(min=8, max=20, message="パスワードは8文字以上20文字以内で入力してください"), EqualTo("confirm_password", message="パスワードが一致しません")])
    # 確認要：パスワード入力
    confirm_password = PasswordField("パスワード確認: ")
    # Email: Email入力
    email = EmailField("メールアドレス: ", validators=[Email("メールアドレスの形式が正しくありません")])
    # 生年月日：日付入力(formatは日付のフォーマットを指定するもの)
    birthday = DateField("生年月日: ", validators=[DataRequired("生年月日は必須入力です")],format="%Y-%m-%d", render_kw={"plaseholder": "（例）yyyy/mm/dd"})
    # 性別：ラジオボタン
    gender = RadioField(
        "性別 :", choices=[("man", "男性"), ("woman", "女性")], default="man"
    )
    # 出身地域：セレクトボックス（choicesは選択肢を指定するもので、選択肢はリストまたはタプル形式で設定する）
    area = SelectField("出身地域: ", choices=[("east", "東日本"), ("west", "西日本")])
    # 既婚: 真偽値入力
    is_married = BooleanField("既婚？: ")
    # メッセージ：複数行テキスト
    note = TextAreaField("備考: ")
    # ボタン
    submit = SubmitField("送信")
    
    
    # 補足：xxxFieldの第一引数はラベル名、第二引数はバリデーションを指定するもの