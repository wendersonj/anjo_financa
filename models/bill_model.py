from math import ceil, floor
from typing import List

from db import db
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String())
    initial_date = db.Column(db.Date())
    final_date = db.Column(db.Date())
    value = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def convert_date_from_str_to_datetime(self, to_date, date_format):
        return datetime.strptime(to_date, date_format)

    def __init__(self, description, initial_date, final_date, value, user_id):
        self.description = description
        self.set_initial_date(initial_date)
        self.set_final_date(final_date)

        if self.initial_date > self.final_date:
            raise ValueError("Data inicial maior que a final.")

        self.user_id = user_id
        self.value = value

    def set_initial_date(self, initial_date):
        if type(initial_date) == str:
            self.initial_date = self.convert_date_from_str_to_datetime(initial_date, DATE_FORMAT)
        else:
            self.initial_date = initial_date

    def set_final_date(self, final_date):
        if type(final_date) == str:
            self.final_date = self.convert_date_from_str_to_datetime(final_date, DATE_FORMAT)
        else:
            self.final_date = final_date

    def __repr__(self):
        return f'<id {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'initial_date': self.initial_date,
            'final_date': self.final_date,
            'value': self.value,
            'user_id': self.user_id
        }

    @property
    def months_in_range(self):
        return max(floor((self.final_date - self.initial_date).days / 30), 1)

    @property
    def total_value(self):
        return self.months_in_range * self.value


def sum_all_bills(bills: List[Bill]):
    return sum(bill.total_value for bill in bills)
