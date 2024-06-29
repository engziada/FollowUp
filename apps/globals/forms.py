from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ProfileActionForm(FlaskForm):
    action_id = SelectField('Action', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('ملاحظات')
    submit = SubmitField('إضافة حدث')
