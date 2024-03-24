from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

# ==============================
# Formクラス
# ==============================
# 入力クラス
class InputForm(FlaskForm): # FlaskFormクラスをflask_wtfから継承
    name = StringField("名前: ", validators=[DataRequired("名前は必須入力です")])
    email = EmailField("メールアドレス: ", validators=[Email("メールアドレスの形式が正しくありません")])
    submit = SubmitField("送信")