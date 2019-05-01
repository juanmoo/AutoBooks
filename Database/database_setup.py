from sqlalchemy import *
from urllib.parse import quote_plus 

# ========== Table Definitions ========== #
metadata = MetaData()

# -- User Table -- #
user_args = [
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('cellphone', String(100)),
    Column('kerberos', String(100)),
    Column('email', String(200))
]
user_table = Table(*user_args)

# -- Officer Table -- #
officer_args = [
    'officer',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('position', String(100), nullable=False),
    Column('brother_id', None, ForeignKey('user.id')),
    Column('year', Integer, nullable=False),
    Column('term', String(100), nullable=False)
]
officer_table = Table(*officer_args)

# -- Transaction Table -- #
transaction_args = [
    'transaction',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('agent', None, ForeignKey('user.id')),
    Column('budget', String(100)),
    Column('year', Integer),
    Column('term', String(100)),
    Column('approver', None, ForeignKey('officer.id')),
    Column('transaction_date', Date),
    Column('amount', Float, nullable=False),
    Column('payment_method', String(100)),
    Column('is_payed', Boolean, nullable=False),
    Column('comment', String(500)),
    Column('receipt_path', String(500)),
    Column('ts', DateTime)
]
transaction_table = Table(*transaction_args)

# -- Payment Table -- #
payment_args = [
    'payment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('ts', DateTime),
    Column('agent', None, ForeignKey('user.id')),
    Column('amount', Float, nullable=False),
    Column('method', String(100)),
    Column('check_number', Integer),
    Column('comment', String(500))
]
payment_table = Table(*payment_args)

# -- Payment-Transaction Table -- #
payment_transaction_args = [
    'payment_transaction',
    metadata,
    Column('payment_id', Integer, ForeignKey('payment.id'), primary_key=True),
    Column('transaction_id', Integer, ForeignKey('transaction.id'), primary_key=True)
]
payment_transaction_table = Table(*payment_transaction_args)


def initialize_database(user, password, host, database, port=3306):
    data = {
        'user':user,
        'password':password,
        'host':host,
        'port':port,
        'dbname':database
    }
    engine_route =  "mysql://{user}:{password}@{host}:{port}/{dbname}".format(**data)

    # Connect to database, initialize tables, and return connection.
    engine = create_engine(engine_route, pool_recycle=3600)
    connection = engine.connect()
    metadata.create_all(engine)

    return connection



if __name__ == "__main__":
    user = 'admin'
    password = 'myPassword'
    host = 'testdb.cfamyzflglg0.us-east-1.rds.amazonaws.com'
    dbname = 'testDB'

    res = initialize_database(user, password, host, dbname)
    print('res:', res)