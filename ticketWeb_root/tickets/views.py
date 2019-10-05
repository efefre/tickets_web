from django.shortcuts import render
from .forms import TicketForm

# Create your views here.
def index(request):
    form = TicketForm()
    return render(request, 'tickets/index.html', {'form':form})
