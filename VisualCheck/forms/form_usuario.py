from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class UsuarioForm(FlaskForm):
    usuario = StringField('Usuário:', validators=[DataRequired()])
    senha = PasswordField('Senha:', validators=[DataRequired()])
    nome = StringField('Nome:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    avatar = IntegerField('Avatar:')
    submit = SubmitField('Cadastrar')

    def clear_fields(self):
        self.usuario.data = ''
        self.senha.data = ''
        self.nome.data = ''
        self.email.data = ''
        self.avatar.data = None

    def fields_as_dict(self, show_passwd=False):
        retorno = {
            'usuario': self.usuario.data,
            'nome': self.nome.data,
            'email': self.email.data,
            'avatar': self.avatar.data
        }
        if show_passwd:
            retorno['senha'] = self.senha.data
        return retorno