import jwt
from functools import wraps
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from flask_cors import cross_origin

import json

auth_blueprint = Blueprint('auth_blueprint', __name__)

from __init__ import db, app
from models import Utilizador


# TODO: Delete and Update

@auth_blueprint.route('/')
def testdb():
    try:
        print(db.session.query(text('show tables')))  # .from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # see Terminal for description of the error
        print("\nThe error:\n" + str(e) + "\n")
        return '<h1>Something is broken.</h1>'


# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'X-Aceess-Token' in request.headers:
            token = request.headers['X-Aceess-Token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Utilizador.query \
                .filter_by(username=data['username']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid!'
            }), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@auth_blueprint.route('/todos', methods=['GET'])
@token_required
def get_all_users(current_user):
    # querying the database
    # for all the entries in it
    users = Utilizador.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append({
            'username': user.username,
            # 'name': user.name,
            'email': user.email,
            'password': user.password
        })

    response = jsonify({'Utilizadores': output})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# route for logging user in
@auth_blueprint.route('/login', methods=['POST'])
@cross_origin()
def login():
    # creates dictionary of form data
    # auth = request.form
    auth = json.loads(request.data)
    if not auth or not auth['email'] or not auth['password']:
        # returns 401 if any email or / and password is missing
        return make_response(
            'Não foi possível verificar o login',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required!"'}
        )

    user = Utilizador.query \
        .filter_by(email=auth['email']) \
        .first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Utilizador não existe',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@auth_blueprint.route('/registo', methods=['POST'])
@cross_origin()
def registar():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    username, email = data.get('username'), data.get('email')
    password = data.get('password')
    firstname=data.get('firstName')
    lastname=data.get('lastName')
    telemovel=data.get('nrTelemovel')
    rat=data.get('rating')
    morad=data.get('morada')
    nascimento=data.get('dataNascimento')
    #avatar
    about=data.get('aboutME')
    # checking for existing user
    user = Utilizador.query \
        .filter_by(email=email) \
        .first()
    if not user:
        # database ORM object
        user = Utilizador(
            username=username,
            # name=name,
            email=email,
            password=generate_password_hash(password),
            firstName=firstname,
            lastName=lastname,
            nrTelemovel=telemovel,
            rating=rat,
            morada=morad,
            dataNascimento=nascimento,
            aboutME=about
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)




@auth_blueprint.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    user = Utilizador.query.filter_by(username=id).first()
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response('Utilizador removido com sucesso.', 200)
 
    return make_response('Utilizador não existe', 204)



#Editar utilizador
@auth_blueprint.route('/<int:id>/update', methods=['GET','POST'])
def updateUser():
    user = Utilizador.query.filter_by(username=id).first()
    data = request.form
    if request.method == 'POST':
        if user:
            db.session.delete(user)
            db.session.commit()
            password = data.get('password')
            firsName = data.get('firstName')
            lastName = data.get('lastName')
            email = data.get('email')
            nrTelemovel = data.get('nrTelemovel')
            #rating
            morada = data.get('morada')
            dataNascimento = data.get('dataNascimento')
            #avatar
            about = data.get('aboutMe')

            user = Utilizador(username=id, password=password, firsName=firsName, lastName=lastName, email=email, nrTelemovel=nrTelemovel, morada=morada,dataNascimento=dataNascimento, aboutMe=about, rating=0)
            db.session.add(user)
            db.session.commit()
        return make_response('Utilizador nao existe', 404)
 
    return make_response('Utilizador atualizado com sucesso', 200)