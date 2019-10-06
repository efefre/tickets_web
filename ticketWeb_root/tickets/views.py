from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import TicketForm
from .utils import Ticket
import datetime

# Create your views here.
def index(request):
    form = TicketForm()
    return render(request, 'tickets/index.html', {'form':form})

def result(request):
    form = TicketForm()

    if request.method == 'POST':
        start_date = request.POST.get("start_date")
        if start_date != '':
            start_date = Ticket.convert_date(start_date)
        stop_date = request.POST.get("stop_date")
        if stop_date != '':
            stop_date = Ticket.convert_date(stop_date)
        cancel_date = request.POST.get("cancel_date")
        if cancel_date != '':
            cancel_date = Ticket.convert_date(cancel_date)
        period = int(request.POST.get("period"))
        ticket_price = float(request.POST.get("ticket_price"))

        if start_date == '':
            start_date = stop_date - datetime.timedelta(days=period) - datetime.timedelta(days=1)

        if stop_date == '':
            stop_date = start_date + datetime.timedelta(days=period) - datetime.timedelta(days=1)

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
