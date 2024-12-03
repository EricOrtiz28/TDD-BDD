# loan_calculator.py

class LoanCalculator:
    def __init__(self, principal, annual_rate, years):
        if principal <= 0:
            raise ValueError("El principal debe ser mayor que cero.")
        if annual_rate < 0:
            raise ValueError("La tasa de interés no puede ser negativa.")
        if years <= 0:
            raise ValueError("El número de años debe ser mayor que cero.")
        self.principal = principal
        self.annual_rate = annual_rate
        self.years = years

    def monthly_payment(self):
        if self.annual_rate == 0:
            return self.principal / (self.years * 12)
        monthly_rate = self.annual_rate / 12 / 100
        payments = self.years * 12
        payment = self.principal * monthly_rate * (1 + monthly_rate) ** payments / ((1 + monthly_rate) ** payments - 1)
        return payment

    def total_payment(self):
        return self.monthly_payment() * self.years * 12

    def total_interest(self):
        return self.total_payment() - self.principal

    def is_affordable(self, monthly_income, other_debts):
        if monthly_income <= 0:
            raise ValueError("El ingreso mensual debe ser mayor que cero.")
        debt_to_income = other_debts / monthly_income
        return debt_to_income < 0.4

    def loan_summary(self, monthly_income, other_debts):
        affordable = self.is_affordable(monthly_income, other_debts)
        summary = {
            'principal': self.principal,
            'annual_rate': self.annual_rate,
            'years': self.years,
            'monthly_payment': round(self.monthly_payment(), 2),
            'total_payment': round(self.total_payment(), 2),
            'total_interest': round(self.total_interest(), 2),
            'affordable': affordable
        }
        return summary