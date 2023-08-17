from django.urls import path

from .views import IndexView, OrderView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('order/', OrderView.as_view(), name='order')
]