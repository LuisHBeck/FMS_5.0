from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Order
from .forms import OrderModelForm


class IndexView(TemplateView):
    template_name = 'index.html'


class OrderView(UserPassesTestMixin, FormView):
    template_name = 'order.html'
    form_class = OrderModelForm
    success_url = reverse_lazy('order')
    login_url = reverse_lazy('index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.requester = self.request.user
        instance.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Error saving')
        return super(OrderView, self).form_valid(form, *args, **kwargs)
    
    def test_func(self):
        return self.request.user.is_authenticated
    

class DemandView(UserPassesTestMixin, TemplateView):
    template_name = 'demand.html'
    login_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(DemandView, self).get_context_data(**kwargs)
        queryset = Order.objects.all()
        selected_filter = self.request.GET.get('filter', None)
        
        if selected_filter:
            queryset = queryset.filter(machine=selected_filter)
        
        context['demand'] = queryset
        return context
    
    def test_func(self):
        return self.request.user.is_authenticated