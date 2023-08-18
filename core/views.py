from django.http import HttpResponse
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import OrderModelForm


class IndexView(TemplateView):
    template_name = 'index.html'


class OrderView(FormView):
    template_name = 'order.html'
    form_class = OrderModelForm
    success_url = reverse_lazy('order')


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.requester = self.request.user
        instance.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)

    
    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Error saving')
        return super(OrderView, self).form_valid(form, *args, **kwargs)