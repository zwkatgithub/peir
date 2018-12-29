from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PNForm(FlaskForm):
    n = IntegerField(validators=[DataRequired(), NumberRange(min=1,max=1000)], default=10)
    submit = SubmitField('提交')
