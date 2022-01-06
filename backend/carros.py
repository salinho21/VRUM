from flask import Blueprint, jsonify, make_response, request
from flask_cors.decorator import cross_origin
from sqlalchemy.sql import text
import base64

carro_blueprint = Blueprint('carro_blueprint', __name__)

from __init__ import db, app
from models import Carro

#TODO

@carro_blueprint.route('/')
def testdb():
    try:
        print(db.session.query(text('show tables')))  # .from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # see Terminal for description of the error
        print("\nThe error:\n" + str(e) + "\n")
        return '<h1>Something is broken.</h1>'


#Obter carros de um utilizador
@carro_blueprint.route('/<string:id>', methods=['GET'])
def get_all_carros(id):
    # querying the database
    # for all the entries in it
    carros=Carro.query.filter(Carro.fk_Utilizador_username==id)

    # converting the query objects
    # to list of jsons
    output = []
    for carro in carros:
        # appending the user data json
        # to the response list
        output.append({
            'matricula': carro.matricula,
            'condutor': carro.fk_Utilizador_username,
            'modelo': carro.modelo,
            'combustivel': carro.tipoFuel,
            'cor': carro.cor,
            'lugares': carro.lugares,
            'foto': carro.foto,
            'ano' : carro.ano
            
        })

    response = jsonify({'Carros': output})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


#Registar um carro
@carro_blueprint.route('/registo', methods=['POST'])
def registar():
    # creates a dictionary of the form data
    data = request.form

    # gets all attributes
    matricula = data.get('matricula')
    condutor = data.get('fk_Utilizador_username')
    modelo = data.get('modelo')
    tipoFuel = data.get('tipoFuel')
    cor = data.get('cor')
    lugares = data.get('lugares')
    ano= data.get('ano')
    
    #foto1= base64.b64decode(data.get('foto'))
    #foto = "".join(["{:08b}".format(x) for x in foto1])
    # checking for existing carro
    carro = Carro.query \
        .filter_by(matricula=matricula) \
        .first()
    if not carro:
        # database ORM object
        carro = Carro(
            matricula = matricula,
            fk_Utilizador_username = condutor,
            modelo = modelo,
            tipoFuel = tipoFuel,
            cor = cor,
            lugares = lugares,
            ano= ano,
            #foto=foto
        )
        # insert carro
        db.session.add(carro)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('Este carro ja existe.', 202)



#Eliminar Carro
@carro_blueprint.route('/<string:matricula>/remove', methods=['Delete'])
def eliminarCarro(matricula):
    if Carro.query.filter_by(matricula=matricula).first() is not None:
        Carro.query.filter_by(matricula=matricula).delete()
        db.session.commit()
        return make_response('Carro removido com sucesso.', 200)
    else:
        return make_response('Carro não existe', 204)



#Editar carro
#/update?matricula=matr
@carro_blueprint.route('/<string:matricula>/update', methods=['Put'])
def updateCarro(matricula):
    
    carro = Carro.query.get(matricula)
    
    if carro is not None:
        data=request.form

    

        for d in data:
            #session.execute(update(stuff_table, values={stuff_table.c.foo: stuff_table.c.foo + 1}))
            setattr(carro,d,data.get(d))
            
        
        db.session.commit()
        

        

        return make_response('Carro atualizado com sucesso', 200)
    else:
        return make_response('Carro nao existe', 404)