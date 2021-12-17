from __init__ import db
from sqlalchemy.dialects.mysql import TINYINT


class Utilizador(db.Model):
    # __tablename__ = 'Utilizador'
    username = db.Column(db.String(45), primary_key=True)
    password = db.Column(db.String(105))
    firstName = db.Column(db.String(45))
    lastName = db.Column(db.String(45))
    email = db.Column(db.String(45))
    nrTelemovel = db.Column(db.String(9))
    rating = db.Column(db.Integer)
    morada = db.Column(db.String(45))
    dataNascimento = db.Column(db.DateTime)
    avatar = db.Column(db.VARBINARY(8000))
    aboutME = db.Column(db.String(200))


class Viagem(db.Model):
    idViagem = db.Column(db.Integer, primary_key=True)
    fk_Carro_matricula = db.Column(db.String(45))
    dataInicio = db.Column(db.DateTime)
    kmsViagem = db.Column(db.Float)
    custoPessoa = db.Column(db.Float)
    localInicio = db.Column(db.String(45))
    bagagem = db.Column(TINYINT(1))
    localDestino = db.Column(db.String(45))
    nrLugares = db.Column(db.Integer)
    lugaresDisp = db.Column(db.Integer)
    regularidade = db.Column(db.String(45))
    idCondutor = db.Column(db.String(45))
    descricao = db.Column(db.String(200))


class Carro(db.Model):
    matricula = db.Column(db.String(45), primary_key=True)
    fk_Utilizador_username = db.Column(db.String(45))
    modelo = db.Column(db.String(45))
    ano = db.Column(db.Integer)
    tipoFuel = db.Column(db.String(45))
    cor = db.Column(db.String(45))
    lugares = db.Column(db.Integer)
    foto = db.Column(db.VARBINARY(8000))


class Avaliacao(db.Model):
    idAvaliacao = db.Column(db.Integer, primary_key=True)
    fk_Viagem_idViagem = db.Column(db.Integer)
    conteudo = db.Column(db.String(45))
    dataAvaliacao = db.Column(db.DateTime)
    utilizador = db.Column(db.String(45))


class Pedido(db.Model):
    idPedido = db.Column(db.Integer, primary_key=True)
    fk_Utilizador_username = db.Column(db.String(45))
    fk_Viagem_idViagem = db.Column(db.Integer)
    nrPessoas = db.Column(db.Integer)
    pickupLocal = db.Column(db.String(45))
    localDestino = db.Column(db.String(45))
    aceite = db.Column(TINYINT(1))

'''
class Usufrui(db.Model):
    fk_Utilizador_username = db.Column(db.String(45))
    fk_Viagem_idViagem = db.Column(db.Integer)
    custoPago = db.Column(db.Float)
'''

class Mensagem(db.Model):
    idMensagem = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(250))
    userOrigem = db.Column(db.String(45))
    userDestino = db.Column(db.String(45))
    data = db.Column(db.DateTime)