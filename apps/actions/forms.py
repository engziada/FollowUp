from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class ActionForm(FlaskForm):
    name = StringField("الحدث", validators=[DataRequired()])
    description = StringField("الوصف")
    steps = StringField("الخطوات")
    due_days = IntegerField("عدد الأيام")
    alert = StringField("التنبيه")
    establishment = StringField("حالة التأسيس")
