from datetime import date

import pytest

from budget_service import Budget, BudgetService


@pytest.mark.parametrize(
    "start, end, budget_statement_list, expected_value",
    [
        (
            date(2024, 1, 1),
            date(2024, 1, 1),
            [("202401", 31)],
            1,
        ),  # test_one_day_amount
        (
            date(2024, 3, 5),
            date(2024, 3, 5),
            [("202403", 62)],
            2,
        ),  # test_one_day_amount_other_than_one
        (
            date(2024, 4, 2),
            date(2024, 4, 7),
            [("202404", 90)],
            18,
        ),  # test_amount_days_in_the_same_month
        (
            date(2024, 5, 1),
            date(2024, 5, 31),
            [("202405", 310)],
            310,
        ),  # test_one_month_amount
        (
            date(2024, 4, 29),
            date(2024, 5, 3),
            [("202404", 90), ("202405", 93)],
            15,
        ),  # test_periods_over_months_with_same_one_day_amount
        (
            date(2024, 4, 29),
            date(2024, 5, 3),
            [("202404", 30), ("202405", 62)],
            8,
        ),  # test_two_months_with_different_one_day_amount
        (
            date(2024, 3, 30),
            date(2024, 5, 5),
            [("202403", 31), ("202404", 60), ("202405", 93)],
            2 * 1 + 60 + 3 * 5,
        ),  # test_periods_over_months_with_different_one_day_amount
        (
            date(2023, 12, 20),
            date(2024, 1, 10),
            [("202312", 31), ("202401", 62)],
            1 * 12 + 2 * 10,
        ),  # test_periods_over_months_in_different_years
        (
            date(2024, 1, 10),
            date(2023, 12, 20),
            [("202312", 31), ("202401", 62)],
            0,
        ),  # test_invalid_period
        (
            date(2023, 12, 20),
            date(2023, 12, 30),
            [("202401", 62)],
            0,
        ),  # test_no_intersection
    ],
)
def test_budget_service(
    start: date, end: date, budget_statement_list: list, expected_value: float
):
    budget_service = BudgetService(budget=Budget(budget_statement_list))
    assert budget_service.get_budget_amount(start=start, end=end) == expected_value
