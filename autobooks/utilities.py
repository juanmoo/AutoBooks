
'''
Functions to facilitate manipulating and adding entries to the database.

Action Descriptions:

User:
1. Create Submission:
    * Provides with query results for the following:
        - Names to find user.id
        - List of budgets
        - Names of officers to select approver

    * takes agent, budget, year, term, approver, transaction_date, amount, payment_method, and a comment to create an entry
2. Register New Users


Admin:
1. Query Transactions -- TODO
2. Create payment
3. Create new user
4. Create new officer

'''

from autobooks.database_setup import initialize_database
from autobooks.database_setup import User, Officer, Transaction, Payment, Payment_Transaction, Category
from datetime import date, datetime
from sqlalchemy.orm import sessionmaker
import json

class DataBase(object):
    def __init__(self, user, password, host, name, port=3306):
        kwargs = {
            'user': user,
            'password': password,
            'host':host,
            'database':name,
            'port':port
        }
        self.engine, self.connection = initialize_database(**kwargs)
        self.Session = sessionmaker(bind=self.engine)

        # Load Categories #
        config_path = "autobooks/config.json"
        with open(config_path, 'r') as config_file:
            payload = config_file.read()
            try:
                config_dict = json.loads(payload)
            except:
                raise Exception("Invalid Configuration File")
        session = self.Session()
        for category_name in config_dict['categories']:
            exists = session.query(Category).filter(Category.name==category_name).first()
            if not exists:
                new_category = Category(name=category_name)
                session.add(new_category)
        session.commit()
        session.close()


    # ===== Admin Functions ===== #
    def create_user(self, first_name, last_name, cellphone='', kerberos='', email=''):

        session = self.Session()
        # Before making new user, check that no other user w/ the same kerberos and or email exists
        
        if len(kerberos) > 0:
           res = list(session.query(User.kerberos).filter(User.kerberos == kerberos))
           if len(res) > 0:
               raise Exception("Kerberos \'%s\' already in database"%kerberos)

        if len(email) > 0:
           res = list(session.query(User.email).filter(User.email == email))
           if len(res) > 0:
               raise Exception("Email already in database")

        if len(cellphone) > 0:
           res = list(session.query(User.cellphone).filter(User.cellphone == cellphone))
           if len(res) > 0:
               raise Exception("Cellphone already in database")
        
        kwargs = {
           'first_name':first_name,
           'last_name':last_name,
           'cellphone':cellphone,
           'kerberos':kerberos,
           'email':email 
        }

        new_user = User(**kwargs)
        session.add(new_user)
        session.commit()
        session.close()
        return new_user
    
    def create_officer(self, user_id, position, year, term):
        session = self.Session()

        kwargs = {
            'user_id':user_id,
            'position':position,
            'year':year,
            'term':term
        }

        new_officer = Officer(**kwargs)
        session.add(new_officer)
        session.commit()
        session.close()

    def create_payment(self, payer, payee, amount, method, transactions, external_id=None, comment=None):

        session = self.Session()

        # Create new payment object
        ts = datetime.now()
        kwargs = {
            'ts':ts,
            'payer':payer,
            'payee':payee,
            'amount':amount,
            'method':method,
            'external_id':external_id,
            'comment':comment
        }

        new_payment = Payment(**kwargs)
        session.add(new_payment)
        session.commit()

        payment_id = new_payment.id

        # Create entries in payment_transaction table
        # transactions is a list of transaction IDs.

        pt_kwargs = [ {'payment_id': payment_id, 'transaction_id':t} for t in transactions ]
        pt_objects = [Payment_Transaction(**kwargs) for kwargs in pt_kwargs]
        session.add_all(pt_objects)
        session.commit()

        session.close()


    # ===== User Functions ===== #
    def create_transaction(self, user_id, budget, year, term, approver_id, transaction_date, amount, payment_method, description, comment, receipt_path, is_payed=False):
        session = self.Session()

        timestamp = datetime.now()
        kwargs = {
            'agent':user_id,
            'budget':budget, 
            'year':year, 
            'term':term, 
            'approver':approver_id, 
            'transaction_date':transaction_date, 
            'amount':amount, 
            'payment_method':payment_method, 
            'comment':comment, 
            'receipt_path':receipt_path,
            'is_payed':is_payed,
            'ts':timestamp,
            'description':description
        }
        
        new_transaction = Transaction(**kwargs)
        session.add(new_transaction)
        session.commit()
        session.close()

if __name__ == '__main__':    
    user = 'root'
    password = 'password'
    host = 'localhost'
    dbname = 'testDB'

    db = DataBase(user, password, host, dbname)

    # Test creating new user
    db.create_user('juan', 'ortiz',  '5136141878', 'juanmoo', 'juanmoo@mit.edu')
    db.create_user('kevin', 'ortiz',  '426436234', 'kevindoo', 'kevindoo@mit.edu')

    # Test creating new officer
    db.create_officer(1, 'treasurer', 2019, 'spring')

    # Test creating a new transaction
    today = date.today()
    res = db.create_transaction(1, 'tech_chair', 2019, 'spring', 1, today, 0.69, 'venmo', 'hello', '~/Documents/Desktop/image')

    # Test creating a payment
    transaction_id = 1
    db.create_payment(1, 2, 2.34, 'venmo', [transaction_id], external_id=None, comment=None)


    print(db.engine, db.connection)
