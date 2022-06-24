from app import DB

class Perfil(DB.Model):
    __tablename__ = 'perfil'
    id            = DB.Column(DB.Integer, primary_key=True)
    nome          = DB.Column(DB.String(32), unique=True, index=True)
    descricao     = DB.Column(DB.String(250))

    acoes         = DB.relationship('PerfilAcao', backref='perfil')

    def __repr__(self):
        return '<Perfil %r>' % self.nome
        
class Usuario(DB.Model):
    __tablename__ = 'usuario'
    id            = DB.Column(DB.Integer, primary_key=True)
    nome          = DB.Column(DB.String(16), unique=True, index=True)
    nome_completo = DB.Column(DB.String(120))

    acoes         = DB.relationship('UsuarioAcao', backref='usuario')

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
