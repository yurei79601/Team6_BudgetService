from calendar import monthrange
from datetime import date
from typing import Dict, List

import pandas as pd


def get_end_of_month(dt: date) -> date:
    return date(
        year=dt.year,
        month=dt.month,
        day=monthrange(dt.year, dt.month)[1],
    )


def get_start_of_month(dt: date) -> date:
    return date(
        year=dt.year,
        month=dt.month,
        day=1,
    )


class Period:
    def __init__(self, start: date, end: date):
        self.start = start
        self.end = end

    def get_days_for_months(self) -> Dict[str, int]:
        date_list = [dt.strftime("%Y%m") for dt in pd.date_range(self.start, self.end)]
        date_distinct_list = sorted(list(set(date_list)))
        return {dt: date_list.count(dt) for dt in date_distinct_list}


def get_intersection_period(first_period: Period, second_period: Period) -> Period:
    return Period(
        start=max(first_period.start, second_period.start),
        end=min(first_period.end, second_period.end),
    )


class OneMonthBudget:
    def __init__(self, year: int, month: int, amount: float):
        self.year = year
        self.month = month
        self.year_month = date(year, month, 1)
        self.amount = amount


class Budget:
    def __init__(self, budget_statement_list: list):
        self.budget_statement_list = budget_statement_list
        self.budgets = self._create_budget(budget_statement_list)
        self.period = self._create_period(budget_statement_list)

    def _create_budget(self, budget_statement_list: list) -> List[OneMonthBudget]:
        return [
            OneMonthBudget(
                year=int(budget_statement[0][:4]),
                month=int(budget_statement[0][4:]),
                amount=budget_statement[1],
            )
            for budget_statement in budget_statement_list
        ]

    def _create_period(self, budget_statement_list: list) -> List[date]:
        first_budget_statment = budget_statement_list[0][0]
        last_budget_statment = budget_statement_list[-1][0]
        return Period(
            start=date(
                int(first_budget_statment[:4]), int(first_budget_statment[4:]), 1
            ),
            end=get_end_of_month(
                date(int(last_budget_statment[:4]), int(last_budget_statment[4:]), 1)
            ),
        )


class BudgetService:
    def __init__(self, budget: Budget):
        self.budget = budget

    def _get_one_day_amount(self, one_mounth_budget: OneMonthBudget) -> float:
        return (
            one_mounth_budget.amount
            / monthrange(
                one_mounth_budget.year_month.year, one_mounth_budget.year_month.month
            )[1]
        )

    def _get_days(self, start: date, end: date) -> int:
        return (end - start).days + 1

    def get_budget_amount(self, start: date, end: date) -> float:
        intersection_period = get_intersection_period(
            Period(start=start, end=end), self.budget.period
        )
        days_months_dict = intersection_period.get_days_for_months()
        total_budget = 0
        for dt, days in days_months_dict.items():
            one_month_budget = [
                budget
                for budget in self.budget.budgets
                if budget.year_month == date(int(dt[:4]), int(dt[4:]), 1)
            ][0]

            total_budget += days * self._get_one_day_amount(one_month_budget)
        return total_budget
