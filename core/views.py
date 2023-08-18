from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from .models import Order
from .forms import OrderModelForm


class IndexView(TemplateView):
    template_name = 'index.html'


class OrderView(FormView):
    template_name = 'order.html'
    form_class = OrderModelForm
    success_url = reverse_lazy('order')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.requester = self.request.user.get_full_name()
        instance.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Error saving')
        return super(OrderView, self).form_valid(form, *args, **kwargs)
    

class DemandView(TemplateView):
    template_name = 'demand.html'

    def get_context_data(self, **kwargs):
        context = super(DemandView, self).get_context_data(**kwargs)
        context['demand'] = Order.objects.all()
        return context