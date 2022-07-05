from datetime import datetime

from config import DB, TAMANHO_CAMPO_EMAIL, TAMANHO_CAMPO_USUARIO
from werkzeug.security import check_password_hash, generate_password_hash


class Usuario(DB.Model):
    __tablename__ = 'usuario'
    id            = DB.Column(DB.Integer, primary_key=True)
    usuario       = DB.Column(DB.String(TAMANHO_CAMPO_USUARIO), unique=True, index=True)
    nome          = DB.Column(DB.String(128), index=True)
    email         = DB.Column(DB.String(TAMANHO_CAMPO_EMAIL), unique=True, index=True)
    avatar        = DB.Column(DB.Integer())
    hash_senha    = DB.Column(DB.String(128))

    @property
    def senha(self):
        raise AttributeError('Senha é um atributo do tipo write-only')

    @senha.setter
    def senha(self, umaSenha):
        self.hash_senha = generate_password_hash(umaSenha,)

    def verifica_senha(self, umaSenha):
        return check_password_hash(self.hash_senha, umaSenha)

