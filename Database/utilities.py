
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
1. Query Transactions
2. Create payment
3. Create new user
4. Create new officer

'''

from database_setup import initialize_database
from database_setup import user_table, officer_table, transaction_table, payment_table, payment_transaction_table
from datetime import date, datetime

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

    # ===== Admin Functions ===== #
    def create_user(self, name, cellphone='', kerberos='', email=''):
        kwargs = {
           'name':name,
           'cellphone':cellphone,
           'kerberos':kerberos,
           'email':email 
        }
        insert = user_table.insert().values(**kwargs)
        res = self.connection.execute(insert)
        return res
    
    def create_officer(self, user_id, position, year, term):
        kwargs = {
            'user_id':user_id,
            'position':position,
            'year':year,
            'term':term
        }
        insert = officer_table.insert().values(**kwargs)
        res = self.connection.execute(insert)
        return res

    def create_payment(self, **kargs):
        # TODO: Define create payment
        pass

    # ===== User Functions ===== #

    def create_transaction(self, user_id, budget, year, term, approver_id, transaction_date, amount, payment_method, comment, receipt_path):
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
            'ts':timestamp
        }
        insert = transaction_table.insert().values(**kwargs)
        res = self.connection.execute(insert)
        return res






if __name__ == '__main__':    
    user = 'admin'
    password = 'myPassword'
    host = 'testdb.cfamyzflglg0.us-east-1.rds.amazonaws.com'
    dbname = 'testDB'

    db = DataBase(user, password, host, dbname)

    # Test creating new user
    db.create_user('juan', '5136141878', 'juanmoo', 'juanmoo@mit.edu')

    # Test creating new officer
    db.create_officer(1, 'treasurer', 2019, 'spring')

    # Test creating a new transaction
    today = date.today()
    db.create_transaction(1, 'tech_chair', 2019, 'spring', 1, today, 0.69, 'venmo', 'hello', '~/Documents/Desktop/image')



    print(db.engine, db.connection)
        