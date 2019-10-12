from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('result', views.result, name='result'),
]
