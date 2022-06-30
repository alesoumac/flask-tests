from config import DB, 
from datetime import datetime

class Usuario(DB.Model):
    __tablename__ = 'usuario'
    id            = DB.Column(DB.Integer, primary_key=True)
    nome          = DB.Column(DB.String(TAMANHO_CAMPO_USUARIO), unique=True, index=True)
    email         = DB.Column(DB.String(TAMANHO_CAMPO_EMAIL), unique=True, index=True)
    nome_completo = DB.Column(DB.String(120))
    confirmado    = DB.Column(DB.Boolean, default=False)
    sobre_mim     = DB.Column(DB.Text())
    membro_desde  = DB.Column(DB.DateTime(), default=datetime.utcnow)
    visto_em      = DB.Column(DB.DateTime(), default=datetime.utcnow)
    hash_pass     = DB.Column(DB.String(128))
    num_avatar    = DB.Column(DB.Integer())

    acoes         = DB.relationship('UsuarioAcao', backref='usuario')

    # def __init__(self, **kwargs):
    #     super(Usuario, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == current_app.config['FLASKY_ADMIN']:
    #             self.role = Role.query.filter_by(name='Administrator').first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()
    #     if self.email is not None and self.avatar_hash is None:
    #         self.avatar_hash = self.gravatar_hash()
    #     self.follow(self)

    @property
    def senha(self):
        raise AttributeError('Não é permitido ler o atributo "senha"')

    @senha.setter
    def senha(self, password):
        self.hash_pass = generate_password_hash(password)

    def verifyica_senha(self, password):
        return check_password_hash(self.hash_pass, password)

