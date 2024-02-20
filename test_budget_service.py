from datetime import datetime
import pytest
from budget_service import BudgetService, Budget


def test_valid_date(mocker):
    budget_service = BudgetService()
    mock_budgets = [Budget(year_month=datetime(2024, 2, 1), amount=310)]
    mocker.patch(
        "budget_service.BudgetService.get_all",
        return_value=mock_budgets,
    )
    actual_value = budget_service.query(datetime(2024, 2, 2), datetime(2024, 2, 1))
    assert actual_value == 0


def test_single_date(mocker):
    budget_service = BudgetService()
    mock_budgets = [Budget(year_month=datetime(2024, 1, 1), amount=31)]
    mocker.patch(
        "budget_service.BudgetService.get_all",
        return_value=mock_budgets,
    )
    actual_value = budget_service.query(datetime(2024, 1, 1), datetime(2024, 1, 1))
    assert actual_value == 1


def test_partial_month_apr(mocker):
    budget_service = BudgetService()
    mock_budgets = [Budget(year_month=datetime(2024, 4, 1), amount=300)]
    mocker.patch(
        "budget_service.BudgetService.get_all",
        return_value=mock_budgets,
    )
    actual_value = budget_service.query(datetime(2024, 4, 1), datetime(2024, 4, 5))
    assert actual_value == 50


def test_partial_month_mar(mocker):
    budget_service = BudgetService()
    mock_budgets = [Budget(year_month=datetime(2024, 3, 1), amount=620)]
    mocker.patch(
        "budget_service.BudgetService.get_all",
        return_value=mock_budgets,
    )
    actual_value = budget_service.query(datetime(2024, 3, 1), datetime(2024, 3, 5))
    assert actual_value == 100


def test_query_for_months(mocker):
    budget_service = BudgetService()
    mock_budgets = [
        Budget(year_month=datetime(2024, 3, 1), amount=620),
        Budget(year_month=datetime(2024, 4, 1), amount=300),
    ]
    mocker.patch(
        "budget_service.BudgetService.get_all",
        return_value=mock_budgets,
    )
    actual_value = budget_service.query(datetime(2024, 3, 30), datetime(2024, 4, 2))
    assert actual_value == 60


def test_no_budget_data(mocker):
    budget_service = BudgetService()
    mock_budgets = [
        Budget(year_month=datetime(2024, 1, 1), amount=31),
        Budget(year_month=datetime(2024, 3, 1), amount=62),
    ]
    mocker.patch(
        "budget_service.BudgetService.get_all",
        return_value=mock_budgets,
    )
    actual_value = budget_service.query(datetime(2024, 2, 1), datetime(2024, 2, 5))
    assert actual_value == 0


def test_query_for_years(mocker):
    budget_service = BudgetService()
    mock_budgets = [
        Budget(year_month=datetime(2023, 12, 1), amount=3100),
        Budget(year_month=datetime(2024, 1, 1), amount=6200),
    ]
    mocker.patch(
        "budget_service.BudgetService.get_all",
        return_value=mock_budgets,
    )
    actual_value = budget_service.query(datetime(2023, 12, 30), datetime(2024, 1, 2))
    assert actual_value == 600
