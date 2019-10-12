from django import forms

class TicketForm(forms.Form):
    start_date = forms.DateField(label='Kiedy aktywowałeś bilet?', input_formats=['%d-%m-%Y',
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
