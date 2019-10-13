from django.shortcuts import render
from django.views import View
from .forms import TicketForm
from .utils import Ticket
import datetime


class IndexView(View):
    form_class = TicketForm
    template_name = 'tickets/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            stop_date = form.cleaned_data["stop_date"]
            cancel_date = form.cleaned_data["cancel_date"]
            period = int(form.cleaned_data["period"])
            ticket_price = float(form.cleaned_data["ticket_price"])

            if start_date == None:
                start_date = stop_date - datetime.timedelta(days=period) + datetime.timedelta(days=1)

            if stop_date == None:
                stop_date = start_date + datetime.timedelta(days=period) - datetime.timedelta(days=1)

            new_ticket = Ticket(start_date, period, stop_date, cancel_date, ticket_price)

            context = new_ticket.count_money_back()

            args =  {'form' : form,
                     'context' : context}

            return render(request, self.template_name, args)
        else:
            return render(request, self.template_name, {'form':form } )
