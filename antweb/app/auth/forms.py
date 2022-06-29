from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email
from wtforms import ValidationError
from ..models.accounts import Usuario, TAMANHO_CAMPO_EMAIL, TAMANHO_CAMPO_USUARIO


class LoginForm(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), Length(1, TAMANHO_CAMPO_USUARIO)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembre_se = BooleanField('Mantenha-me logado')
    submit = SubmitField('Fazer Login')


class RegistrationForm(FlaskForm):
    usuario = StringField('Usuário', validators=[
        DataRequired(), Length(1, TAMANHO_CAMPO_USUARIO),
        Regexp('^[A-Za-z][A-Za-z0-9]*$', 0,
               'Nome de usuário só pode conter letras ou números ')])
    email = StringField('Email', validators=[DataRequired(), Length(1, TAMANHO_CAMPO_EMAIL),
                                             Email()])
    senha = PasswordField('Senha', validators=[
        DataRequired(), EqualTo('senha2', message='Senhas não conferem.')])
    senha2 = PasswordField('Confirme a senha', validators=[DataRequired()])
    submit = SubmitField('Registrar Usuário')

    def validar_email(self, field):
        if Usuario.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email já registrado.')

    def validar_usuario(self, field):
        if Usuario.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


# class ChangePasswordForm(FlaskForm):
#     old_password = PasswordField('Old password', validators=[DataRequired()])
#     password = PasswordField('New password', validators=[
#         DataRequired(), EqualTo('password2', message='Passwords must match.')])
#     password2 = PasswordField('Confirm new password',
#                               validators=[DataRequired()])
#     submit = SubmitField('Update Password')


# class PasswordResetRequestForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Length(1, 64),
#                                              Email()])
#     submit = SubmitField('Reset Password')


# class PasswordResetForm(FlaskForm):
#     password = PasswordField('New Password', validators=[
#         DataRequired(), EqualTo('password2', message='Passwords must match')])
#     password2 = PasswordField('Confirm password', validators=[DataRequired()])
#     submit = SubmitField('Reset Password')


# class ChangeEmailForm(FlaskForm):
#     email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
#                                                  Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Update Email Address')

#     def validate_email(self, field):
#         if User.query.filter_by(email=field.data.lower()).first():
#             raise ValidationError('Email already registered.')
