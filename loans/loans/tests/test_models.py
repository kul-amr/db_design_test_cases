from ..backend.models import User,Report,Loan,ReportLoan
from sqlalchemy.exc import IntegrityError
import pytest

#test that seeds a database with sample data for each type
def test_data_create(session):

    u1 = User(name='test u1',email='test1@g.com')
    l1 = Loan(balance=2345)
    l2 = Loan(balance=2345,currency='USD')
    session.add_all([u1,l1,l2])
    session.commit()

    usrs = User.query.all()
    assert len(usrs) == 1
    assert usrs[0].name == 'test u1'

    loans = Loan.query.all()
    assert len(loans )==2
    assert loans[0].currency == 'GBP'
    assert loans[1].currency == 'USD'

    r1 = Report(title='test_report',body='test report body',author=usrs[0].id)
    session.add(r1)
    session.commit()
    reports = Report.query.all()
    assert len(reports) == 1
    assert reports[0].author == usrs[0].id

    rl = ReportLoan(report=reports[0].id,loan=loans[0].id)
    session.add(rl)
    session.commit()

    reportloans=ReportLoan.query.all()

    assert len(reportloans)==1
    assert reportloans[0].report == reports[0].id
    assert reportloans[0].loan == loans[0].id

#test case that ensures the constraints work as expected - User
def test_user_create_exceptions(session):

    u2 = User(email='em@h.com')
    session.add(u2)

    with pytest.raises(IntegrityError) as err:
        session.commit()
    if err.value.message:
        session.rollback()

    assert err.value.message
    assert len(User.query.all()) == 0

#test case that ensures the constraints work as expected - Loan
def test_loan_create_exceptions(session):
    l1 = Loan(balance=2345,currency='XYZ')
    l2 = Loan(balance=-234)
    session.add(l1)

    with pytest.raises(IntegrityError) as err:
        session.commit()
    if err.value.message:
        session.rollback()

    assert err.value.message
    assert len(Loan.query.all())==0

    session.add(l2)
    with pytest.raises(IntegrityError) as err:
        session.commit()
    if err.value.message:
        session.rollback()

    assert err.value.message
    assert len(Loan.query.all()) == 0

#test case that ensures the relationships work as expected - Report
def test_report_create_exceptions(session):

    u1 = User(name='test u1', email='test1@g.com')
    session.add(u1)
    session.commit()

    r1 = Report(body='test report',author=u1.id)
    session.add(r1)

    with pytest.raises(IntegrityError) as err:
        session.commit()
    if err.value.message:
        session.rollback()

    assert err.value.message
    assert len(Report.query.all()) == 0

    r2 = Report(title='test_report',body='test report', author=15)
    session.add(r2)

    with pytest.raises(IntegrityError) as err:
        session.commit()
    if err.value.message:
        session.rollback()

    assert err.value.message
    assert len(Report.query.all()) == 0

#test case that ensures the relationships work as expected - ReportLoan
def test_reportloan_create_exception(session):

    rl = ReportLoan(report=5, loan=7)
    session.add(rl)

    with pytest.raises(IntegrityError) as err:
        session.commit()
    if err.value.message:
        session.rollback()

    assert err.value.message
    assert len(ReportLoan.query.all()) == 0

