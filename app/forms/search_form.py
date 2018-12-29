from flask_wtf import FlaskForm
from wtforms import  SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, NumberRange, Length


class SearchForm(FlaskForm):
    type_ = SelectField('搜索类型',
                        coerce=int, choices=list(zip([0,1,2],['自动','严格','宽松'])), default=0)
    disease = StringField('病名', validators=[Length(min=0,max=300)])
    gene = StringField('基因', validators=[Length(min=0, max=300)])

    submit = SubmitField('检索')
