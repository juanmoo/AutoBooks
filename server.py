#! /usr/bin/python3
'''

Application Webserver

'''

from flask import Flask, request
import autobooks.utilities as util
from autobooks.database_setup import *

app = Flask(__name__)

## Start DB ##
db = util.DataBase(
        'root',
        'password',
        'localhost',
        'testDB'
    )



@app.route('/')
def home():
    return "Hello Diana!"

@app.route('/users', methods=['GET', 'POST'])
def users():
    action = request.args.get('action', 'none')

    if (action == 'new_user'):
        # TODO: AUTH

        # Get Params
        first = request.args.get('first', '')
        last = request.args.get('last', '')
        cellphone = request.args.get('cellphone', '')
        email = request.args.get('email', '')
        kerberos = request.args.get('kerberos', '')

        # Create user entry in DB
        session = db.Session()
        try:
            new_user = db.create_user(first, last, cellphone=cellphone, kerberos=kerberos, email=email)
        except:
            return "User already in database"
        session.close()
        return "New User Added"

    elif(action == 'new_officer'):
        # TODO: AUTH

        # Get Params
        email = request.args.get('email', None)
        position = request.args.get('position', None)
        year = request.args.get('year', None)
        term = request.args.get('term', None)
        if any(e is None for e in [email, position, year, term]):
            # Error: Missing Arguments
            return "Missing Required Arguments"


        # Create Officer
        session = db.Session()
        res = session.query(User.id, User.first_name).filter(User.email==email).all()
        if len(res) < 1:
            return "No such user"
        uid, first = res[0]
        session.close()

        try:
            res = db.create_officer(uid, position, year, term)
        except:
            return 'Error creating new officer.'

        return 'New ' + position + ' created  for ' + first + '.'


    elif(action == 'list_all'):
        session = db.Session()
        res = session.query(User.first_name, User.last_name)
        session.close()
        return str(list(res))

    return "Nothing Happened"

