from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus 

# ========== Table Definitions ========== #
metadata = MetaData()
Base = declarative_base()

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

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    cellphone = Column(String(100))
    kerberos = Column(String(100))
    email = Column(String(200))

# -- Officer Table -- #
officer_args = [
    'officer',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('position', String(100), nullable=False),
    Column('user_id', None, ForeignKey('user.id')),
    Column('year', Integer, nullable=False),
    Column('term', String(100), nullable=False)
]
officer_table = Table(*officer_args)

class OfficerTable(Base):
    __tablename__ = 'officer'
    id = Column(Integer, primary_key=True)
    position = Column(String(100), nullable=False)
    user_id = Column(None, ForeignKey('user.id'))
    year = Column(Integer, nullable=False)
    term = Column(String(100), nullable=False)

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
class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column( Integer, primary_key=True )
    agent = Column( None, ForeignKey('user.id') )
    budget = Column( String(100) )
    year = Column( Integer )
    term = Column( String(100) )
    approver = Column( None, ForeignKey('officer.id') )
    transaction_date = Column( Date )
    amount = Column( Float, nullable=False )
    payment_method = Column( String(100) )
    is_payed = Column( Boolean, nullable=False )
    comment = Column( String(500) )
    receipt_path = Column( String(500) )
    ts = Column( DateTime )

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

class Payment(Base):
    __tablename__ = 'payment'

    id = Column( Integer, primary_key=True )
    ts = Column( DateTime )
    agent = Column( None, ForeignKey('user.id') )
    amount = Column( Float, nullable=False )
    method = Column( String(100) )
    check_number = Column( Integer )
    comment = Column( String(500) )

# -- Payment-Transaction Table -- #
payment_transaction_args = [
    'payment_transaction',
    metadata,
    Column('payment_id', Integer, ForeignKey('payment.id'), primary_key=True),
    Column('transaction_id', Integer, ForeignKey('transaction.id'), primary_key=True)
]
payment_transaction_table = Table(*payment_transaction_args)

class Payment_Transaction(Base):
    __tablename__ = 'payment_transaction'

    payment_id = Column( Integer, ForeignKey('payment.id'), primary_key=True )
    transaction_id = Column( Integer, ForeignKey('transaction.id'), primary_key=True )


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
    Base.metadata.create_all(engine)
    #metadata.create_all(engine)

    return (engine, connection)



if __name__ == "__main__":
    user = 'admin'
    password = 'myPassword'
    host = 'testdb.cfamyzflglg0.us-east-1.rds.amazonaws.com'
    dbname = 'testDB'

    res = initialize_database(user, password, host, dbname)
    print('res:', res)