from typing import List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Budget:
    year_month: datetime
    amount: int

class BudgetService:
    def get_all(self, start, end) -> List[Budget]:
        pass

    def query(self, start, end):
        return 0
