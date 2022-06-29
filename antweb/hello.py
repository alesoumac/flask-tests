from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('Nome:', validators=[DataRequired()])
    age = IntegerField('Idade:', validators=[DataRequired()])
    #birth_date = DateTimeLocalField('Data de Nascimento:', format="%d/%m/%Y")
    submit = SubmitField('Submit')
