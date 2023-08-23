from django.views.generic import TemplateView, FormView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator

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
        return super(OrderView, self).form_invalid(form, *args, **kwargs)
    
    def test_func(self):
        return self.request.user.is_authenticated
    

class DemandView(UserPassesTestMixin, TemplateView):
    template_name = 'demand.html'
    login_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(DemandView, self).get_context_data(**kwargs)
        queryset = Order.objects.all()
        selected_filter = self.request.GET.get('filter', None)    
        
        # FILTER
        if selected_filter:
            queryset = queryset.filter(machine=selected_filter)
            
        context['demand'] = queryset
        
        # PAGINATION
        paginator = Paginator(queryset, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        
        return context
    
    def test_func(self):
        return self.request.user.is_authenticated
    

class OrderEditView(UserPassesTestMixin, UpdateView):
    template_name = 'order_edit.html'
    form_class = OrderModelForm
    login_url = ('index')
    model = Order

    def get_success_url(self):
        return reverse('order_edit', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Error Updating')
        return super().form_invalid(form, *args, **kwargs)
    
    def test_func(self):
        return self.request.user.is_authenticated
    

# class AccountView(TemplateView):
#     template_name = 'account.html'
