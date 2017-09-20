from models import User,Report,Loan,ReportLoan

def get_all_report_for_loan(loan_id):
    all_reports_set = ReportLoan.query.filter_by(loan=loan_id).all()
    all_reports = [i.report for i in all_reports_set]

    return all_reports

def get_sum_loans_for_report(report_id):
    all_loans_set = ReportLoan.query.filter_by(report=report_id).all()
    all_loans = [{Loan.query.filter_by(id=i.loan).all()[0].currency :
                  Loan.query.filter_by(id=i.loan).all()[0].balance} for i in all_loans_set]
    loan_amount = dict()
    for i in all_loans:
        key_currency=i.keys()[0]
        if key_currency in loan_amount:
            loan_amount[key_currency] +=i.get(key_currency)
        else:
            loan_amount[key_currency] = i.get(key_currency)

    return loan_amount