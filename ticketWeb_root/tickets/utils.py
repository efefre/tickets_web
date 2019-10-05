import datetime

class Ticket:
    #handling fee is 20% but not more than 50 zl
    handling_fee_percent = 0.2

    def __init__(self, start_date = None, day = 0, end_date = None, cancel_date = None, ticket_price = None):
        self.start_date = start_date
        self.day = day
        self.end_date = end_date
        self.cancel_date = cancel_date
        self.money_back = None
        self.ticket_price = ticket_price

    @staticmethod
    def convert_date(date):
        year, month, day = date.split('-')
        return datetime.date(int(year), int(month), int(day))

    def count_money_back(self):
        self.handling_fee = self.handling_fee_percent * float(self.ticket_price)
        if self.handling_fee > 50:
            self.handling_fee = 50

        self.cancled_days = self.end_date - self.cancel_date
        self.money_back = round(float((self.ticket_price - self.handling_fee)/self.day * int(self.cancled_days.days)),2)

        result = {
            'start_date': self.start_date,
            'stop_date': self.end_date,
            'cancel_date': self.cancel_date,
            'period': self.day,
            'one_day_cost': (self.ticket_price - self.handling_fee) / self.day,
            'handling_fee': self.handling_fee,
            'money_back': self.money_back,
            'costs_incurred': self.ticket_price - self.money_back
        }

        return result


    def __str__(self):
        return 'Nowy bilet {} - {} (dni: {})'.format(self.start_date, self.end_date, self.day)
