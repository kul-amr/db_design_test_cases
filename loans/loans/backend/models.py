from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, String, Float, CheckConstraint, Text, ForeignKey
import datetime as dt


#new sqlalchemy object
db = SQLAlchemy()

#creating abstract base model for other models to inherit from
class Base(db.Model):
    __abstract__ = True
    id = Column(Integer,primary_key=True,autoincrement=True)
    create_date = Column(DateTime,default=dt.datetime.utcnow())
    update_date = Column(DateTime, default=dt.datetime.utcnow())

#model for User
class User(Base):
    __tablename__ = 'users'
    name = Column(String(255),nullable=False)
    email = Column(String(50),nullable=False,unique=True)

    def __repr__(self):
        return self.name

#model for Loan
class Loan(Base):
    __tablename__ = 'loans'
    currency = Column(String(5),default='GBP')
    balance = Column(Float)

    __table_args__ = (CheckConstraint(balance >= 0, name='check_balance_positive'),
                      CheckConstraint(currency.in_(['USD','GBP','JPY']),name='check_currency_list'))

    def __repr__(self):
        return 'id:%r balance:%r' % (self.id, self.balance)

#model for Report
class Report(Base):
    __tablename__ = 'reports'
    title = Column(String(255),nullable=False)
    body = Column(Text,default='')
    author = Column(Integer,ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        return self.title

#model for ReportLoan to store various loans against report
class ReportLoan(db.Model):
    __tablename__ = 'reportloans'
    report = Column(Integer,ForeignKey('reports.id'),primary_key=True)
    loan = Column(Integer,ForeignKey('loans.id'),primary_key=True)

    def __repr__(self):
        return 'report: %r loan:%r' % (self.report , self.loan)
