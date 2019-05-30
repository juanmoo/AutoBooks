#! /usr/bin/python3
'''

Application Webserver

'''

from flask import Flask, request
from flask_cors import CORS
import autobooks.utilities as util
from autobooks.database_setup import *
from urllib.parse import quote
import json
import datetime

app = Flask(__name__)
CORS(app)

## Start DB ##
db = util.DataBase(
        'root',
        'password',
        'localhost',
        'testDB'
    )


@app.route('/reimbursements', methods=['GET', 'POST'])
def reimbursements():

    if request.method == 'GET':
        action = request.args.get('action', 'none')
        if (action == 'get_form_info'):
            info = {}
            session = db.Session()
            # Get ID, NAME for all users
            res = session.query(User.id, User.first_name, User.last_name).all()
            users = {e[0]:"{first} {last}".format(first=e[1].strip(), last=e[2].strip()) for e in res}
            info['users'] = users

            # Get Categories
            res = session.query(Category.id, Category.name).all()
            categories = {e[0]: e[1] for e in res}
            info['categories'] = categories

            # Get Officers
            res = session.query(Officer.id, Officer.position, User.first_name, User.last_name).\
                    filter(Officer.user_id == User.id).all()
            officers = {e[0]: "{first} {last} - {title}".format(first=e[2], last=e[3], title=e[1]) for e in res}
            info['officers'] = officers

            session.close()

            return json.dumps(info)

    elif request.method == 'POST':
        res = request.form
        
        uid = int(res['user'])
        budget = int(res['budget'])
        datestring = res['date']
        trans_date = datetime.datetime.strptime(datestring, "%Y-%m-%d").date()
        year = 2019
        term = 'SPRING'
        officer = int(res['officer'])
        amount = float(res['amount'])
        payment_method = res['payment_method']
        comment = res['comment']
        receipt_path = ''
        description = res['description']


        # Create the new transaction
        db.create_transaction(uid, budget, year, term, officer, trans_date, amount, payment_method, description, comment, receipt_path)


        return str(res)

    return "There be Dragons HERE"




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
        res = session.query(User.id, User.first_name, User.last_name).all()
        session.close()
        names = {e[0]:"{first} {last}".format(first=e[1].strip(), last=e[2].strip()) for e in res}
        out = {'names':names}
        return json.dumps(out)

    
    return "Nothing Happened"


