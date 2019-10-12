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
        val_1, val_2, val_3 = date.split('-')
        # Chrome/Brave/Firefox
        if len(val_1) == 4:
            year = val_1
            day = val_3
        # Safari
        else:
            day = val_1
            year = val_3
        month = val_2

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
            'one_day_cost': round((self.ticket_price - self.money_back) / int((self.cancel_date-self.start_date).days +1),2),
            'handling_fee': self.handling_fee,
            'money_back': self.money_back,
            'costs_incurred': round(self.ticket_price - self.money_back,2)
        }

        return result


    def __str__(self):
        return 'Nowy bilet {} - {} (dni: {})'.format(self.start_date, self.end_date, self.day)
