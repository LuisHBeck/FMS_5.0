from django.shortcuts import render

from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from .forms import Order

class IndexView(TemplateView):
    template_name = 'index.html'

class OrderView(FormView):
    template_name = 'order.html'
    form_class = Order
    reverse_url = reverse_lazy('index')