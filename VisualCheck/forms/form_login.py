from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    usuario = StringField('Usuário:', validators=[DataRequired()])
    senha = PasswordField('Senha:', validators=[DataRequired()])
    #submit = SubmitField('Entrar')

    def clear_fields(self):
        self.usuario.data = ''
        self.senha.data = ''

    def fields_as_dict(self, show_passwd=False):
        retorno = { 'usuario': self.usuario.data }
        if show_passwd:
            retorno['senha'] = self.senha.data
        return retorno