from database import db_session
from models import User, Accounts, Categories, Transactions, Goals

def populate():
    #u = User('Sean','Johnson','seanjohnson20@gmail.com','pass')
    #db_session.add(u)
  
    db_session.add_all([
        User('demo','demo','demo@mail.com','pass'),
        User('sean','johnson','seanjohnson20@gmail.com','pass'),
        
        Accounts('Savings','demo@mail.com'),
        Accounts('Checking','demo@mail.com'),
        Accounts('Cash','demo@mail.com'),
        
        Categories('Emergency','demo@mail.com'),
        Categories('Vacation','demo@mail.com'),
        Categories('Car Repair','demo@mail.com'),
        Categories('Car Registration','demo@mail.com'),
        Categories('Car Replace','demo@mail.com'),
        Categories('Christmas','demo@mail.com'),
        Categories('Birthday','demo@mail.com'),
        
        Goals('demo@mail.com','Emergency','2013-01-01','Minimum Balance', 1000.00),
        Goals('demo@mail.com','Car Replace','2018-07-01','New truck in 5 yrs', 8000.00),
        Goals('demo@mail.com','Car Registration','2014-07-01','Annual Registration', 125.00),
        Goals('demo@mail.com','Car Repair','2013-09-01','Keep car running w/o debt', 500.00),
        Goals('demo@mail.com','Vacation','2014-08-30','Caribbean or Bust', 4000.00),
        
        Transactions('demo@mail.com','Savings','Emergency','Minimum Balance','2013-07-01', 'Its a start', 100.00),
        Transactions('demo@mail.com','Checking','Car Replace','New truck','2013-07-01','4x4',300.00),
        Transactions('demo@mail.com','Cash','Birthday','','2013-07-01','Suprise',150.00),
        Transactions('demo@mail.com','Savings','Vacation','Caribbean or Bust','2013-07-01', 'Its a start',100.00),
        Transactions('demo@mail.com','Savings','Emergency','','2013-07-01', 'Darn',-200.00),
        Transactions('demo@mail.com','Savings','Emergency','','2013-07-01', 'Building Emerg fund again',300.00),
        Transactions('demo@mail.com','Savings','Vacation','Caribbean or Bust' ,'2013-07-01', 'cant wait',300.00),
        Transactions('demo@mail.com','Savings','Emergency','Minimum Balance','2013-07-01', 'Its a start',100.00),
        Transactions('demo@mail.com','Checking','Car Replace','','2013-07-01', 'New truck',900.00),
        Transactions('demo@mail.com','Cash','Birthday','','2013-07-01', 'Suprise', 150.00),
        Transactions('demo@mail.com','Savings','Car Registration','Annual Registration','2013-07-01', 'Its a start',100.00),
        Transactions('demo@mail.com','Savings','Emergency','','2013-07-01', 'Darn',-200.00),
        Transactions('demo@mail.com','Savings','Emergency','Minimum Balance','2013-07-01', 'Building Emerg fund again',300.00),
        Transactions('demo@mail.com','Savings','Car Repair','Keep car running w/o debt','2013-07-01','cant wait',300.00),
        ])
    
    db_session.commit()

populate()