from flask_wtf import FlaskForm
from wtforms import StringField,DateField,EmailField,TextAreaField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    name = StringField("الجهة", validators=[DataRequired()])
    about = TextAreaField("نبذه", validators=[Length(max=500)])
    est_date = DateField("تاريخ التأسيس")
    account_manager = StringField("مدير الحساب")
    account_manager_email = EmailField("البريد الإلكتروني لمدير الحساب")
    phones = StringField("الهواتف")
    address = StringField("العنوان")
