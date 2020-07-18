from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateItemForm(FlaskForm):
    content = StringField('Content*', validators=[DataRequired()])
    submit = SubmitField('Create!', render_kw={
        'class': 'btn btn-primary btn-lg btn-block'
    })
