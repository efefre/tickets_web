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
                start_date = stop_date - datetime.timedelta(days=period) - datetime.timedelta(days=1)

            if stop_date == None:
                stop_date = start_date + datetime.timedelta(days=period) - datetime.timedelta(days=1)

            new_ticket = Ticket(start_date, period, stop_date, cancel_date, ticket_price)

            context = new_ticket.count_money_back()

            args =  {'form' : form,
                     'context' : context}

            return render(request, self.template_name, args)
        else:
            return render(request, self.template_name, {'form':form } )

        if cancel_date < start_date:
            messages.error(request, 'Wprowadzono błędną datę. Nie można zwrócić biletu przed jego aktywacją')
            return redirect(reverse('tickets:index'))

        if cancel_date > stop_date:
            messages.error(request, 'Wprowadzono błędną datę. Nie można zwrócić biletu po terminie ważności')
            return redirect(reverse('tickets:index'))

        if period != 30 and period != 90:
            messages.error(request, 'Wprowadzono błędną wartość. Dozwolone wartości: 30 albo 90')
            return redirect(reverse('tickets:index'))

        new_ticket = Ticket(start_date, period, stop_date, cancel_date, ticket_price)

        context = new_ticket.count_money_back()

        return render(request, 'tickets/result.html', {'context': context})
    else:
        form = TicketForm()
        return redirect('/')
