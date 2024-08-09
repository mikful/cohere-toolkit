from typing import Any, Dict, List
from dataclasses import dataclass
from backend.tools.base import BaseTool
from py_expression_eval import Parser

@dataclass
class LoanDetails:
    loan_amount: float
    term_years: int
    interest_rate: float

    def monthly_payment(self) -> float:
        monthly_rate = self.interest_rate / 12 / 100
        num_payments = self.term_years * 12
        return (self.loan_amount * monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

class LoanRefinanceCalculator(BaseTool):
    """
    Function Tool that calculates loan refinancing options.
    """

    NAME = "toolkit_loan_refinance_calculator"

    @classmethod
    def is_available(cls) -> bool:
        return True

    def calculate_refinance(self, current_loan: LoanDetails, refi_loan: LoanDetails, years_paid: int, closing_costs_percent: float, finance_closing_costs: bool, cash_out_amount: float) -> Dict[str, Any]:
        # Calculate remaining balance on current loan
        remaining_balance = current_loan.loan_amount * ((1 + current_loan.interest_rate/12/100)**(current_loan.term_years*12) - (1 + current_loan.interest_rate/12/100)**(years_paid*12)) / ((1 + current_loan.interest_rate/12/100)**(current_loan.term_years*12) - 1)

        # Calculate new loan amount
        new_loan_amount = remaining_balance + cash_out_amount
        if finance_closing_costs:
            closing_costs = new_loan_amount * closing_costs_percent / 100
            new_loan_amount += closing_costs

        refi_loan.loan_amount = new_loan_amount

        return {
            "original_monthly_payment": round(current_loan.monthly_payment(), 2),
            "refinanced_monthly_payment": round(refi_loan.monthly_payment(), 2)
        }

    async def call(self, parameters: dict, **kwargs: Any) -> List[Dict[str, Any]]:
        # Extract parameters
        original_loan_amount = float(parameters.get("original_loan_amount", 0))
        original_term = int(parameters.get("original_term", 0))
        years_paid = int(parameters.get("years_paid", 0))
        original_interest_rate = float(parameters.get("original_interest_rate", 0))

        refi_term = int(parameters.get("refi_term", 0))
        refi_interest_rate = float(parameters.get("refi_interest_rate", 0))
        closing_costs_percent = float(parameters.get("closing_costs_percent", 0))
        finance_closing_costs = parameters.get("finance_closing_costs", "").lower() == "yes"
        cash_out_amount = float(parameters.get("cash_out_amount", 0))

        # Create loan objects
        current_loan = LoanDetails(original_loan_amount, original_term, original_interest_rate)
        refi_loan = LoanDetails(0, refi_term, refi_interest_rate)  # Loan amount will be calculated in refinance function

        # Calculate refinance options
        result = self.calculate_refinance(current_loan, refi_loan, years_paid, closing_costs_percent, finance_closing_costs, cash_out_amount)

        return [{"result": result}]