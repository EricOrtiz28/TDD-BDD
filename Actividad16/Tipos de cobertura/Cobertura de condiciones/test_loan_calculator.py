# test_loan_calculator.py

import pytest
from loan_calculator import LoanCalculator

@pytest.fixture
def calculator():
    return LoanCalculator(principal=100000, annual_rate=5, years=30)

def test_initialization_valid():
    loan = LoanCalculator(200000, 3.5, 15)
    assert loan.principal == 200000
    assert loan.annual_rate == 3.5
    assert loan.years == 15

def test_initialization_invalid_principal():
    with pytest.raises(ValueError) as excinfo:
        LoanCalculator(0, 5, 30)
    assert "El principal debe ser mayor que cero." in str(excinfo.value)

def test_initialization_invalid_rate():
    with pytest.raises(ValueError) as excinfo:
        LoanCalculator(100000, -1, 30)
    assert "La tasa de interés no puede ser negativa." in str(excinfo.value)

def test_initialization_invalid_years():
    with pytest.raises(ValueError) as excinfo:
        LoanCalculator(100000, 5, 0)
    assert "El número de años debe ser mayor que cero." in str(excinfo.value)

def test_monthly_payment_non_zero_rate(calculator):
    payment = calculator.monthly_payment()
    assert round(payment, 2) == 536.82

def test_monthly_payment_zero_rate():
    loan = LoanCalculator(120000, 0, 30)
    payment = loan.monthly_payment()
    assert payment == 120000 / (30 * 12)

def test_total_payment(calculator):
    total = calculator.total_payment()
    assert round(total, 2) == 193255.78

def test_total_interest(calculator):
    interest = calculator.total_interest()
    assert round(interest, 2) == 93255.78

def test_is_affordable_true(calculator):
    assert calculator.is_affordable(monthly_income=5000, other_debts=1000) == True

def test_is_affordable_false(calculator):
    assert calculator.is_affordable(monthly_income=3000, other_debts=1500) == False

def test_is_affordable_zero_income(calculator):
    with pytest.raises(ValueError) as excinfo:
        calculator.is_affordable(monthly_income=0, other_debts=500)
    assert "El ingreso mensual debe ser mayor que cero." in str(excinfo.value)

def test_loan_summary_affordable(calculator):
    summary = calculator.loan_summary(monthly_income=6000, other_debts=1000)
    assert summary['affordable'] == True

def test_loan_summary_not_affordable(calculator):
    summary = calculator.loan_summary(monthly_income=3000, other_debts=1500)
    assert summary['affordable'] == False

def test_loan_summary_zero_rate():
    loan = LoanCalculator(120000, 0, 30)
    summary = loan.loan_summary(monthly_income=4000, other_debts=1000)
    assert round(summary['monthly_payment'], 2) == round(120000 / (30 * 12), 2)
    assert summary['affordable'] == True

def test_loan_summary_high_debts(calculator):
    summary = calculator.loan_summary(monthly_income=4000, other_debts=1600)
    assert summary['affordable'] == False

def test_loan_summary_low_debts(calculator):
    summary = calculator.loan_summary(monthly_income=8000, other_debts=2000)
    assert summary['affordable'] == True

def test_loan_summary_invalid_income(calculator):
    with pytest.raises(ValueError) as excinfo:
        calculator.loan_summary(monthly_income=-1000, other_debts=500)
    assert "El ingreso mensual debe ser mayor que cero." in str(excinfo.value)