from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired


class UsuarioForm(FlaskForm):
    usuario = StringField('Usuário:', validators=[DataRequired()])
    senha = HiddenField('Senha:',validators=[DataRequired()])
    nome = StringField('Nome:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    avatar = IntegerField('Avatar:')
    submit = SubmitField('Submit')