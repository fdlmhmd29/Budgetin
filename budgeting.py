# budgeting.py

from datetime import datetime, timedelta
from constants import TARIF, MAP_HARI
from utils import date_range

class BudgetCalculator:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start = start_date
        self.end   = end_date
        self.total_krl     = 0
        self.total_krd     = 0
        self.daily_logs    = []  # tuples (date, hari, krl, krd)
        self.weekly_summary = []  # tuples (week_num, week_start, week_end, sum_krl, sum_krd)

    def calculate(self):
        week_num   = 1
        week_start = self.start

        for current in date_range(self.start, self.end):
            kode = current.weekday()
            hari = MAP_HARI[kode]
            krl  = TARIF[hari]['krl']
            krd  = TARIF[hari]['krd']

            self.total_krl += krl
            self.total_krd += krd
            self.daily_logs.append((current, hari, krl, krd))

            if kode == 5 or current == self.end:
                wk_krl = sum(log[2] for log in self.daily_logs if week_start <= log[0] <= current)
                wk_krd = sum(log[3] for log in self.daily_logs if week_start <= log[0] <= current)
                self.weekly_summary.append((week_num, week_start, current, wk_krl, wk_krd))
                week_num   += 1
                week_start  = current + timedelta(days=1)

    @property
    def total(self) -> int:
        return self.total_krl + self.total_krd
