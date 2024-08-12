import pytest
from community.tools import LoanRefinanceCalculator

def test_loan_refinance_calculator_basic():
    calculator = LoanRefinanceCalculator()
    loan_data = {
        "original_loan_amount": 100000,
        "original_term": 30,
        "years_paid": 3,
        "original_interest_rate": 6.5,
        "refi_term": 30,
        "refi_interest_rate": 3,
        "closing_costs_percent": 3.5,
        "finance_closing_costs": True,
        "cash_out_amount": 0
    }
    
    result = calculator.call(parameters=loan_data)
    
    assert "result" in result
    assert isinstance(result["result"], dict)
    assert "original_monthly_payment" in result["result"]
    assert "refinanced_monthly_payment" in result["result"]
    assert "remaining_interest_original" in result["result"]
    assert "refinanced_total_interest" in result["result"]
    
    # Check if refinanced monthly payment is lower
    assert result["result"]["refinanced_monthly_payment"] < result["result"]["original_monthly_payment"]
    
    # Check if refinanced total interest is lower
    assert result["result"]["refinanced_total_interest"] < result["result"]["remaining_interest_original"]

def test_loan_refinance_calculator_cash_out():
    calculator = LoanRefinanceCalculator()
    loan_data = {
        "original_loan_amount": 200000,
        "original_term": 30,
        "years_paid": 5,
        "original_interest_rate": 4.5,
        "refi_term": 25,
        "refi_interest_rate": 3.75,
        "closing_costs_percent": 2,
        "finance_closing_costs": True,
        "cash_out_amount": 20000
    }
    
    result = calculator.call(parameters=loan_data)
    
    assert "result" in result
    assert isinstance(result["result"], dict)
    assert result["result"]["refinanced_total_payable"] > result["result"]["remaining_payable_original"]

def test_loan_refinance_calculator_no_benefit():
    calculator = LoanRefinanceCalculator()
    loan_data = {
        "original_loan_amount": 150000,
        "original_term": 30,
        "years_paid": 10,
        "original_interest_rate": 3.5,
        "refi_term": 20,
        "refi_interest_rate": 4.0,
        "closing_costs_percent": 3,
        "finance_closing_costs": False,
        "cash_out_amount": 0
    }
    
    result = calculator.call(parameters=loan_data)
    
    assert "result" in result
    assert isinstance(result["result"], dict)
    assert result["result"]["refinanced_monthly_payment"] > result["result"]["original_monthly_payment"]
    assert result["result"]["refinanced_total_interest"] > result["result"]["remaining_interest_original"]

def test_loan_refinance_calculator_invalid_input():
    calculator = LoanRefinanceCalculator()
    loan_data = {
        "original_loan_amount": "invalid",
        "original_term": 30,
        "years_paid": 3,
        "original_interest_rate": 6.5,
        "refi_term": 30,
        "refi_interest_rate": 3,
        "closing_costs_percent": 3.5,
        "finance_closing_costs": True,
        "cash_out_amount": 0
    }
    
    result = calculator.call(parameters=loan_data)
    
    assert "text" in result
    assert "Invalid value" in result["text"]

def test_loan_refinance_calculator_missing_parameter():
    calculator = LoanRefinanceCalculator()
    loan_data = {
        "original_loan_amount": 100000,
        "original_term": 30,
        "years_paid": 3,
        "original_interest_rate": 6.5,
        "refi_term": 30,
        "refi_interest_rate": 3,
        "closing_costs_percent": 3.5,
        "finance_closing_costs": True
        # Missing cash_out_amount
    }
    
    result = calculator.call(parameters=loan_data)
    
    assert "result" in result
    assert isinstance(result["result"], dict)
    # The call should succeed with a default value for cash_out_amount