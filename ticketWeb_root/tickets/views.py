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
        start_date = Ticket.convert_date(request.POST.get("start_date"))
        stop_date = Ticket.convert_date(request.POST.get("stop_date"))
        cancel_date = Ticket.convert_date(request.POST.get("cancel_date"))
        period = int(request.POST.get("period"))
        ticket_price = float(request.POST.get("ticket_price"))

        if start_date == None:
            start_date = stop_date - datetime.timedelta(days=period) - datetime.timedelta(days=1)

        if stop_date == None:
            stop_date = start_date + datetime.timedelta(days=period) - datetime.timedelta(days=1)

        if cancel_date < start_date:
            # 'Wprowadzono błędną datę. Nie można zwrócić biletu przed jego aktywacją'
            return redirect(reverse('tickets:index'))

        new_ticket = Ticket(start_date, period, stop_date, cancel_date, ticket_price)

        context = new_ticket.count_money_back()

        return render(request, 'tickets/result.html', {'context': context})
    else:
        form = TicketForm()
        return redirect('/')
