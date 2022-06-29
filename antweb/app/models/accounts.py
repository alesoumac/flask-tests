from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from markdown import markdown
#import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from .. import db as DB
from .. import login_manager

TAMANHO_CAMPO_EMAIL = 80
TAMANHO_CAMPO_USUARIO = 16

class Perfil(DB.Model):
    __tablename__ = 'perfil'
    id            = DB.Column(DB.Integer, primary_key=True)
    nome          = DB.Column(DB.String(32), unique=True, index=True)
    descricao     = DB.Column(DB.String(250))

    acoes         = DB.relationship('PerfilAcao', backref='perfil')

    def __repr__(self):
        return '<Perfil %r>' % self.nome
        
class Usuario(UserMixin, DB.Model):
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

    def gera_token_confirmacao(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmado = True
        DB.session.add(self)
        return True

    def gera_token_reset(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_senha(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = Usuario.query.get(data.get('reset'))
        if user is None:
            return False
        user.senha = new_password
        DB.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        #self.avatar_hash = self.gravatar_hash()
        DB.session.add(self)
        return True

    def can(self, perm):
        return True
        # return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return True
        # return self.can(Permission.ADMIN)

    def ping(self):
        self.visto_em = datetime.utcnow()
        DB.session.add(self)

    # def gravatar_hash(self):
    #     return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    # def gravatar(self, size=100, default='identicon', rating='g'):
    #     url = 'https://secure.gravatar.com/avatar'
    #     hash = self.avatar_hash or self.gravatar_hash()
    #     return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
    #         url=url, hash=hash, size=size, default=default, rating=rating)

    # def follow(self, user):
    #     if not self.is_following(user):
    #         f = Follow(follower=self, followed=user)
    #         db.session.add(f)

    # def unfollow(self, user):
    #     f = self.followed.filter_by(followed_id=user.id).first()
    #     if f:
    #         db.session.delete(f)

    # def is_following(self, user):
    #     if user.id is None:
    #         return False
    #     return self.followed.filter_by(
    #         followed_id=user.id).first() is not None

    # def is_followed_by(self, user):
    #     if user.id is None:
    #         return False
    #     return self.followers.filter_by(
    #         follower_id=user.id).first() is not None

    # @property
    # def followed_posts(self):
    #     return Post.query.join(Follow, Follow.followed_id == Post.author_id)\
    #         .filter(Follow.follower_id == self.id)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'nome': self.nome,
            'nome_completo': self.nome_completo,
            'membro_desde': self.membro_desde,
            'visto_em': self.visto_em,
            'email': self.email
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return Usuario.query.get(data['id'])

    def __repr__(self):
        return '<Usuario %r>' % self.nome

class Acao(DB.Model):
    __tablename__ = 'acao'
    id            = DB.Column(DB.Integer, primary_key=True)
    descricao     = DB.Column(DB.String(128), unique=True, index=True)
    grupo         = DB.Column(DB.String(32))

    perfis        = DB.relationship('PerfilAcao',  backref='acao')
    usuarios      = DB.relationship('UsuarioAcao', backref='acao')

    def __repr__(self):
        return '<Acao %r>' % self.descricao

class PerfilAcao(DB.Model):
    __tablename__ = 'perfil_acao'
    id        = DB.Column(DB.Integer, primary_key=True)
    id_perfil = DB.Column(DB.Integer, DB.ForeignKey('perfil.id'))
    id_acao   = DB.Column(DB.Integer, DB.ForeignKey('acao.id'))

    def __repr__(self):
        return '<Perfil %r :: Acao %r>' % (self.id_perfil, self.id_acao)

class UsuarioAcao(DB.Model):
    __tablename__ = 'usuario_acao'
    id         = DB.Column(DB.Integer, primary_key=True)
    id_usuario = DB.Column(DB.Integer, DB.ForeignKey('usuario.id'))
    id_acao    = DB.Column(DB.Integer, DB.ForeignKey('acao.id'))

    def __repr__(self):
        return '<Usuario %r :: Acao %r>' % (self.id_usuario, self.id_acao)
