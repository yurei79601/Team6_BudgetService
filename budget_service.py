from typing import List
from dataclasses import dataclass
from calendar import monthrange
from datetime import datetime


@dataclass
class Budget:
    year_month: datetime
    amount: int


class BudgetService:
    def get_all(self, start, end) -> List[Budget]:
        pass

    def query(self, start, end):
        if start > end:
            return 0
        total_budget = 0
        monthly_budgets = self.get_all()
        for budget in monthly_budgets:
            budget_year = budget.year_month.year
            budget_month = budget.year_month.month
            days_in_month = monthrange(budget_year, budget_month)[1]

            if (
                start.year <= budget_year <= end.year
                and start.month <= budget_month <= end.month
            ):
                if budget_year == start.year and budget_month == start.month:
                    if start.month == end.month and start.year == end.year:
                        days_count = end.day - start.day + 1
                    else:
                        days_count = days_in_month - start.day + 1
                    daily_budget = budget.amount / days_in_month
                    total_budget += daily_budget * days_count
                elif budget_year == end.year and budget_month == end.month:
                    daily_budget = budget.amount / days_in_month
                    total_budget += daily_budget * end.day
                else:
                    total_budget += budget.amount

        return total_budget
