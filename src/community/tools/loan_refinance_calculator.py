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

    def total_payable(self) -> float:
        return self.monthly_payment() * self.term_years * 12

    def total_interest(self) -> float:
        return self.total_payable() - self.loan_amount

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

        # Calculate total amount paid so far on the original loan
        total_paid_so_far = current_loan.monthly_payment() * years_paid * 12

        # Calculate remaining payable on the original loan
        remaining_payable_original = current_loan.total_payable() - total_paid_so_far

        # Calculate remaining interest on the original loan
        remaining_interest_original = remaining_payable_original - remaining_balance

        # Calculate total interest on the refinanced loan
        total_interest_refi = refi_loan.total_interest()

        return {
            "original_monthly_payment": round(current_loan.monthly_payment(), 2),
            "original_total_payable": round(current_loan.total_payable(), 2),
            "remaining_payable_original": round(remaining_payable_original, 2),
            "remaining_interest_original": round(remaining_interest_original, 2),
            "refinanced_monthly_payment": round(refi_loan.monthly_payment(), 2),
            "refinanced_total_payable": round(refi_loan.total_payable(), 2),
            "refinanced_total_interest": round(total_interest_refi, 2)
        }

    async def call(self, parameters: dict, **kwargs: Any) -> List[Dict[str, Any]]:
        # Extract parameters with error checking
        def get_param(key, type_func, default=None):
            value = parameters.get(key, default)
            if value is None:
                print(f"Missing required parameter: {key}")
            try:
                return type_func(value)
            except ValueError:
                print(f"Invalid value for {key}: {value}")

        original_loan_amount = get_param("original_loan_amount", int)
        original_term = get_param("original_term", int)
        years_paid = get_param("years_paid", int)
        original_interest_rate = get_param("original_interest_rate", float)

        refi_term = get_param("refi_term", int)
        refi_interest_rate = get_param("refi_interest_rate", float)
        closing_costs_percent = get_param("closing_costs_percent", float)
        finance_closing_costs = parameters.get("finance_closing_costs", bool)
        cash_out_amount = get_param("cash_out_amount", int, 0)

        # Create loan objects
        current_loan = LoanDetails(original_loan_amount, original_term, original_interest_rate)
        refi_loan = LoanDetails(0, refi_term, refi_interest_rate)  # Loan amount will be calculated in refinance function

        # Calculate refinance options
        try:
            result = {"result": self.calculate_refinance(current_loan, refi_loan, years_paid, closing_costs_percent, finance_closing_costs, cash_out_amount)}
        except Exception as e:
            print(f"[LoanRefinanceCalculator] Error parsing expression: {e}")
            result = {"text": str(e)}

        return result
    

## Use the following params to test (from the Default settings on the website)
#     loan_data = {
#         "original_loan_amount": 100000,
#         "original_term": 30,
#         "years_paid": 3,
#         "original_interest_rate": 6.5,
#         "refi_term": 30,
#         "refi_interest_rate": 3,
#         "closing_costs_percent": 3.5,
#         "finance_closing_costs": "yes",
#         "cash_out_amount": 0
#     }

## in the chatbot ui use the following to test it's extraction capabilities
# The amount of cash you want to take out in the refinance: $0
# The closing costs as a percentage of the new loan amount: 3.5%
# Whether you want to finance the closing costs in the new loan amount: Yes
# The original interest rate of the loan: 6.5%
# The original amount of the loan: $100,000
# The original term of the loan: 30 years
# The interest rate of the refinanced loan: 3
# The term of the refinanced loan: 30 years
# The number of years already paid on the original loan: 3 years