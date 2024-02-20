from datetime import datetime
import pytest
from budget_service import BudgetService


def test_singel_date(mocker):
    budget_service = BudgetService()
    mocker.patch(
        "budget_service.BudgetService.get_all",
        return_value=[{"year_month": datetime(2024, 1, 0), "amount": 31}],
    )
    actual_value = budget_service.query(datetime(2024, 1, 1), datetime(2024, 1, 1))
    assert actual_value == 1
