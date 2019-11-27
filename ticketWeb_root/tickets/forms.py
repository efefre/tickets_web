import datetime

from django import forms


class TicketForm(forms.Form):
    start_date = forms.DateField(label='Kiedy aktywowałaś/aktywowałeś bilet?', input_formats=['%d-%m-%Y',
                                                                                  '%Y-%m-%d'],
                                 widget=forms.DateInput(format=('%d-%m-%Y'),
                                                        attrs={'placeholder': 'dd-mm-rrrr',
                                                               'class':'form-control',
                                                               'type':'date'}),
                                 required=False)
    stop_date = forms.DateField(label='Do kiedy bilet jest ważny?', input_formats=['%d-%m-%Y',
                                                                                   '%Y-%m-%d'],
                                 widget=forms.DateInput(format=('%d-%m-%Y'),
                                                        attrs={'placeholder': 'dd-mm-rrrr',
                                                               'class':'form-control',
                                                               'type':'date'}),
                                required=False)
    cancel_date = forms.DateField(label='Data anulowania biletu.', input_formats=['%d-%m-%Y',
                                                                                  '%Y-%m-%d'],
                                widget=forms.DateInput(format=('%d-%m-%Y'),
                                                       attrs={'placeholder': 'dd-mm-rrrr',
                                                              'class': 'form-control',
                                                              'type': 'date'}))
    PERIOD_CHOICES = [
        (30, '30 dni'),
        (90, '90 dni')
    ]
    period = forms.ChoiceField(label='Okres obowiązywania biletu.', choices=PERIOD_CHOICES,
                               widget= forms.Select(attrs={'class':'form-control'}))

    ticket_price = forms.FloatField(label='Ile zapłaciłaś/zapłaciłeś za bilet?',
                                    widget=forms.NumberInput(attrs={'class':'form-control',
                                                                    'step':0.01}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        stop_date = cleaned_data.get('stop_date')
        cancel_date = cleaned_data.get('cancel_date')
        period = int(cleaned_data.get('period'))
        ticket_price = float(cleaned_data.get('ticket_price'))

        if start_date == None and stop_date == None:
            msg ='Musisz podać datę aktywacji bilet albo do kiedy bilet jest ważny'
            self.add_error(None, msg)

        if start_date != None and stop_date != None:
            if start_date >= stop_date:
                self.add_error('start_date', 'Data aktywacji biletu nie może być późniejsza niż data końca ważności biletu.')
                self.add_error('stop_date', 'Data końca ważności biletu nie może być wcześniejsza niż data aktywacji biletu.')

            start_date_including_period = stop_date - datetime.timedelta(days=period) + datetime.timedelta(days=1)
            stop_date_including_period = start_date + datetime.timedelta(days=period) - datetime.timedelta(days=1)

            if start_date != start_date_including_period or stop_date != stop_date_including_period:
                self.add_error('start_date',
                               'Między datą aktywacji biletu, a datą ważności biletu nie ma {} dni.'.format(period))
                self.add_error('stop_date',
                               'Między datą aktywacji biletu, a datą ważności biletu nie ma {} dni.'.format(period))

        if start_date != None:
            if start_date >= cancel_date:
                self.add_error('start_date', 'Data aktywacji biletu nie może być późniejsza niż data anulowania biletu.')
                self.add_error('cancel_date', 'Data anulowania biletu nie może być wcześniejsza niż data aktywacji biletu.')

        if stop_date != None:
            if stop_date < cancel_date:
                self.add_error('stop_date',
                               'Data końca ważności biletu nie może być wcześniejsza niż data anulowania biletu.')
                self.add_error('cancel_date',
                               'Data anulowania biletu nie może być późniejsza niż data końca ważności biletu.')
            elif stop_date.year > cancel_date.year:
                self.add_error('stop_date',
                               'Zwróć uwagę na rok w podanych datach.')
                self.add_error('cancel_date',
                               'Zwróć uwagę na rok w podanych datach.')
            elif start_date == None:
                start_date = stop_date - datetime.timedelta(days=period) + datetime.timedelta(days=1)
                if start_date >= cancel_date:
                    self.add_error('cancel_date',
                                   f'Bilet był aktywowany: {start_date.strftime("%d-%m-%Y")}. Data anulowania biletu nie może być wcześniejsza niż data aktywacji biletu.')

        if ticket_price <= 0:
            self.add_error('ticket_price',
                           'Wprowadź poprawną cenę (większą od 0).')