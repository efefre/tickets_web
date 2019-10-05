from django import forms

class TicketForm(forms.Form):
    start_date = forms.DateField(label='Kiedy aktywowałeś bilet?', input_formats='%d-%m-%Y',
                                 widget=forms.DateInput(format=('%d-%m-%Y'),
                                                        attrs={'placeholder': 'dd-mm-rrrr',
                                                               'class':'form-control',
                                                               'type':'date'}),
                                 required=False)
    stop_date = forms.DateField(label='Do kiedy bilet jest ważny?', input_formats='%d-%m-%Y',
                                 widget=forms.DateInput(format=('%d-%m-%Y'),
                                                        attrs={'placeholder': 'dd-mm-rrrr',
                                                               'class':'form-control',
                                                               'type':'date'}),
                                required=False)
    cancel_date = forms.DateField(label='Data anulowania biletu.', input_formats='%d-%m-%Y',
                                widget=forms.DateInput(format=('%d-%m-%Y'),
                                                       attrs={'placeholder': 'dd-mm-rrrr',
                                                              'class': 'form-control',
                                                              'type': 'date'}))
    period = forms.IntegerField(label='Okres obowiązywania biletu.', min_value=30, max_value=90,
                                widget=forms.NumberInput(attrs={'placeholder':'30 albo 90 dni',
                                                                'class':'form-control'}),
                                required=False)
    ticket_price = forms.FloatField(label='Ile zapłaciłaś/zapłaciłeś za bilet?',
                                    widget=forms.NumberInput(attrs={'class':'form-control',
                                                                    'step':0.01}))
