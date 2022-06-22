from db_global import DB, BASE_DIR

class Perfil(DB.Model):
    __tablename__ = 'perfil'
    id = DB.Column(DB.Integer, primary_key=True)
    nome = DB.Column(DB.String(32), unique=True, index=True)
    descricao = DB.Column(DB.String(250))

    def __repr__(self):
        return '<Perfil %r>' % self.nome
        
class Usuario(DB.Model):
    __tablename__ = 'usuario'
    id = DB.Column(DB.Integer, primary_key=True)
    nome = DB.Column(DB.String(16), unique=True, index=True)
    nome_completo = DB.Column(DB.String(120))

    def __repr__(self):
        return '<Usuario %r>' % self.nome

class Acao(DB.Model):
    __tablename__ = 'acao'
    id = DB.Column(DB.Integer, primary_key=True)
    descricao = DB.Column(DB.String(128), unique=True, index=True)
    grupo = DB.Column(DB.String(32))

    def __repr__(self):
        return '<Acao %r>' % self.descricao
