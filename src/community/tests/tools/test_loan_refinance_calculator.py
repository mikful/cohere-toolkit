# from community.tools import LoanRefinanceCalculator
# import json
# import pytest

# @pytest.fixture
# def calculator():
#     return LoanRefinanceCalculator()

# def test_basic_refinance(calculator):
#     # these are the default values on the website calculator to test against
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
    
#     result = calculator.calculate_from_json(json.dumps(loan_data))
    
#     assert isinstance(result, dict)
#     assert "original_monthly_payment" in result
#     assert "refinanced_monthly_payment" in result
#     assert "remaining_balance" in result
#     assert "new_loan_amount" in result
    
#     assert result["original_monthly_payment"] > result["refinanced_monthly_payment"]
#     assert result["new_loan_amount"] > result["remaining_balance"]

# def test_no_cashout_no_closing_costs(calculator):
#     loan_data = {
#         "original_loan_amount": 300000,
#         "original_term": 30,
#         "years_paid": 10,
#         "original_interest_rate": 5.0,
#         "refi_term": 20,
#         "refi_interest_rate": 3.5,
#         "closing_costs_percent": 1.5,
#         "finance_closing_costs": "no",
#         "cash_out_amount": 0
#     }
    
#     result = calculator.calculate_from_json(json.dumps(loan_data))
    
#     assert isinstance(result, dict)
#     assert result["new_loan_amount"] == pytest.approx(result["remaining_balance"], rel=1e-9)

# def test_invalid_input(calculator):
#     loan_data = {
#         "original_loan_amount": "invalid",
#         "original_term": 30,
#         "years_paid": 5,
#         "original_interest_rate": 4.5,
#         "refi_term": 25,
#         "refi_interest_rate": 3.75,
#         "closing_costs_percent": 2,
#         "finance_closing_costs": "yes",
#         "cash_out_amount": 10000
#     }
    
#     with pytest.raises(ValueError):
#         calculator.calculate_from_json(json.dumps(loan_data))

# def test_edge_case_zero_values(calculator):
#     loan_data = {
#         "original_loan_amount": 0,
#         "original_term": 0,
#         "years_paid": 0,
#         "original_interest_rate": 0,
#         "refi_term": 0,
#         "refi_interest_rate": 0,
#         "closing_costs_percent": 0,
#         "finance_closing_costs": "no",
#         "cash_out_amount": 0
#     }
    
#     result = calculator.calculate_from_json(json.dumps(loan_data))
    
#     assert isinstance(result, dict)
#     assert result["original_monthly_payment"] == 0
#     assert result["refinanced_monthly_payment"] == 0
#     assert result["remaining_balance"] == 0
#     assert result["new_loan_amount"] == 0

# def test_large_values(calculator):
#     loan_data = {
#         "original_loan_amount": 10000000,
#         "original_term": 30,
#         "years_paid": 1,
#         "original_interest_rate": 10,
#         "refi_term": 29,
#         "refi_interest_rate": 9.5,
#         "closing_costs_percent": 5,
#         "finance_closing_costs": "yes",
#         "cash_out_amount": 1000000
#     }
    
#     result = calculator.calculate_from_json(json.dumps(loan_data))
    
#     assert isinstance(result, dict)
#     assert result["original_monthly_payment"] > 0
#     assert result["refinanced_monthly_payment"] > 0
#     assert result["remaining_balance"] > 0
#     assert result["new_loan_amount"] > result["remaining_balance"]