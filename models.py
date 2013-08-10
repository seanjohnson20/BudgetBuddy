from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

from werkzeug import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    firstname = Column(String(50), unique=False)
    lastname = Column(String(50), unique=False)
    email = Column(String(120), unique=True)
    pwdhash = Column('password', String(20), nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<email %r>' % (self.email)
        
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
  
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String, ForeignKey('users.email'), nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<name %r>' % (self.name)

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String, ForeignKey('users.email'), nullable=False)


    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<name %r>' % (self.name)
        
class Goals(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    email = Column(String, ForeignKey('users.email'), nullable=False)
    category = Column(String, ForeignKey('categories.name'), nullable=False)
    target = Column(String(10), nullable=True)
    description = Column(String(200), unique=False)
    amount = Column(Float(precision=2), nullable=True)

    def __init__(self, email, category, target, description, amount):
        self.email = email 
        self.category = category
        self.target = target
        self.description = description
        self.amount = amount

    def __repr__(self):
        return '<description %r>' % (self.description)
        
class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    email = Column(String, ForeignKey('users.email'), nullable=False)
    account = Column(String, ForeignKey('accounts.name'), nullable=False)
    category = Column(String, ForeignKey('categories.name'), nullable=False)
    goal = Column(String, ForeignKey('goals.description'), nullable=True)
    trans_date = Column(String(10), nullable=False)
    notes = Column(String(200), unique=False)
    amount = Column(Float(precision=2), nullable=False)

    def __init__(self, email, account, category, goal, trans_date, notes, amount):
        self.email = email
        self.account = account  # FOREIGN KEY
        self.category = category  # FOREIGN KEY
        self.goal = goal  # FOREIGN KEY
        self.trans_date = trans_date
        self.notes = notes
        self.amount = amount

    def __repr__(self):
        return '<notes %r>' % (self.notes)