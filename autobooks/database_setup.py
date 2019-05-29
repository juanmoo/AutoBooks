from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus 

# ========== Table Definitions ========== #
Base = declarative_base()

# -- Categories -- #
# This tables stores the names of the different budgets #
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    __table_args__ = (UniqueConstraint('name'),)

# -- User Table -- #
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    cellphone = Column(String(100))
    kerberos = Column(String(100))
    email = Column(String(200))

# -- Officer Table -- #
class Officer(Base):
    __tablename__ = 'officer'
    id = Column(Integer, primary_key=True)
    position = Column(String(100), nullable=False)
    user_id = Column(None, ForeignKey('user.id'))
    year = Column(Integer, nullable=False)
    term = Column(String(100), nullable=False)

    # ARGS #
    __table_args__ = (UniqueConstraint('user_id', 'year', 'term', 'position'),)

# -- Transaction Table -- #
class Transaction(Base):
    # Metadata #
    __tablename__ = 'transaction'

    # IDs #
    id = Column( Integer, primary_key=True )
    agent = Column( None, ForeignKey('user.id') )
    approver = Column( None, ForeignKey('officer.id'), default=None)
    budget = Column( String(100) )
    year = Column( Integer )
    term = Column( String(100) )

    # Monetary #
    amount = Column( Float, nullable=False )
    payment_method = Column( String(100) )
    is_payed = Column( Boolean, nullable=False )
    
    # Date #
    transaction_date = Column( Date )
    approval_date = Column ( DateTime, default=None )
    ts = Column( DateTime )

    # Other #
    description = Column( String(500) )
    comment = Column( String(500) )
    receipt_path = Column( String(500) )

# -- Payment Table -- #
class Payment(Base):
    # Metadata #
    __tablename__ = 'payment'

    # IDs #
    id = Column( Integer, primary_key=True )
    payer = Column( None, ForeignKey('user.id') )
    payee = Column( None, ForeignKey('user.id') )
    approver = Column( None, ForeignKey('officer.id' ))

    # Monetary #
    amount = Column( Float, nullable=False )
    method = Column( String(100) )
    external_id = Column( Integer )

    # Date/Time #

    ts = Column( DateTime )

    # Other #
    comment = Column( String(500) )

# -- Payment-Transaction Table -- #
class Payment_Transaction(Base):
    __tablename__ = 'payment_transaction'
    payment_id = Column( Integer, ForeignKey('payment.id'), primary_key=True )
    transaction_id = Column( Integer, ForeignKey('transaction.id'), primary_key=True )


# -- Creates instance of database and passes connection -- #
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

    return (engine, connection)



if __name__ == "__main__":
    user = 'root'
    password = 'password'
    host = 'localhost'
    dbname = 'testDB'

    res = initialize_database(user, password, host, dbname)
    print('res:', res)

