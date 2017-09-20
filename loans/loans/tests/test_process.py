from ..backend.models import User,Report,Loan,ReportLoan
from ..backend import process


#test case for finding all reports that a loan belongs to
def test_get_all_report_for_loan(session):
    u1 = User(id=1,name='test u1', email='test1@g.com')
    l1 = Loan(id=100,balance=2345)
    l2 = Loan(id=101,balance=234, currency='USD')
    session.add_all([u1,l1,l2])
    session.commit()

    usrs = User.query.all()
    loans= Loan.query.all()

    r1 = Report(id=10,title='test_report1', body='test report body', author=usrs[0].id)
    r2 = Report(id=11,title='test_report2', body='test report body', author=usrs[0].id)
    r3 = Report(id=12,title='test_report3', body='test report body', author=usrs[0].id)
    session.add_all([r1,r2,r3])
    session.commit()
    reports = Report.query.all()

    rl1 = ReportLoan(report=reports[0].id,loan=loans[0].id)
    rl2 = ReportLoan(report=reports[1].id,loan=loans[0].id)
    rl3 = ReportLoan(report=reports[0].id,loan=loans[1].id)
    rl4 = ReportLoan(report=reports[2].id, loan=loans[1].id)
    session.add_all([rl1,rl2,rl3,rl4])
    session.commit()

    all_reports = process.get_all_report_for_loan(loan_id=loans[0].id)

    assert len(all_reports)==2
    assert reports[0].id in all_reports
    assert reports[1].id in all_reports
    assert reports[2].id not in all_reports

#test case for calculating the sum of all loans that went into a specific report
def test_get_sum_loans_for_report(session):
    u1 = User(id=5, name='test u1', email='test1@g.com')
    l1 = Loan(id=500, balance=2000, currency='USD')
    l2 = Loan(id=501, balance=3000, currency='USD')
    l3 = Loan(id=502, balance=6000)
    session.add_all([u1,l1,l2,l3])
    session.commit()

    users = User.query.all()
    loans = Loan.query.all()

    r1 = Report(id=5000, title='test_report1', body='test report body', author=users[0].id)
    r2 = Report(id=5001, title='test_report2', body='test report body', author=users[0].id)
    r3 = Report(id=5002, title='test_report3', body='test report body', author=users[0].id)
    session.add_all([r1,r2,r3])
    session.commit()
    reports = Report.query.all()

    rl1 = ReportLoan(report=reports[0].id, loan=loans[0].id)
    rl2 = ReportLoan(report=reports[0].id, loan=loans[1].id)
    rl3 = ReportLoan(report=reports[0].id, loan=loans[2].id)
    rl4 = ReportLoan(report=reports[1].id, loan=loans[2].id)
    session.add_all([rl1, rl2, rl3, rl4])
    session.commit()

    sum_amount = process.get_sum_loans_for_report(report_id=r1.id)
    assert sum_amount.get('USD') == 5000
    assert sum_amount.get('GBP') == 6000
