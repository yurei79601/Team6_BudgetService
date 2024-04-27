from datetime import date

from budget_service import Budget, BudgetService


def test_one_day_amount():
    budget_statement_list = [("202401", 31)]
    budget_service = BudgetService(budget=Budget(budget_statement_list))
    start = date(2024, 1, 1)
    assert budget_service.get_budget_amount(start=start, end=start) == 1


def test_one_day_amount_other_than_one():
    budget_statement_list = [("202403", 62)]
    budget_service = BudgetService(budget=Budget(budget_statement_list))
    start = date(2024, 3, 5)
    assert budget_service.get_budget_amount(start=start, end=start) == 2


def test_amount_days_in_the_same_month():
    budget_statement_list = [("202404", 90)]
    budget_service = BudgetService(budget=Budget(budget_statement_list))
    start = date(2024, 4, 2)
    end = date(2024, 4, 7)
    assert budget_service.get_budget_amount(start=start, end=end) == 18


def test_one_month_amount():
    budget_statement_list = [("202405", 310)]
    budget_service = BudgetService(budget=Budget(budget_statement_list))
    start = date(2024, 5, 1)
    end = date(2024, 5, 31)
    assert budget_service.get_budget_amount(start=start, end=end) == 310


def test_periods_over_months_with_same_one_day_amount():
    budget_statement_list = [("202404", 90), ("202405", 93)]
    budget_service = BudgetService(budget=Budget(budget_statement_list))
    start = date(2024, 4, 29)
    end = date(2024, 5, 3)
    assert budget_service.get_budget_amount(start=start, end=end) == 15


def test_two_months_with_different_one_day_amount():
    budget_statement_list = [("202404", 30), ("202405", 62)]
    budget_service = BudgetService(budget=Budget(budget_statement_list))
    start = date(2024, 4, 29)
    end = date(2024, 5, 3)
    assert budget_service.get_budget_amount(start=start, end=end) == 8


def test_periods_over_months_with_different_one_day_amount():
    budget_statement_list = [("202403", 31), ("202404", 60), ("202405", 93)]
    budget_service = BudgetService(budget=Budget(budget_statement_list))
    start = date(2024, 3, 30)
    end = date(2024, 5, 5)
    assert budget_service.get_budget_amount(start=start, end=end) == 2 * 1 + 60 + 3 * 5
