from django.urls import path

from .views import IndexView, OrderView, DemandView, OrderEditView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('order/', OrderView.as_view(), name='order'),
    path('demand/', DemandView.as_view(), name='demand'),
    path('order/<int:pk>/edit/', OrderEditView.as_view(), name='order_edit'),
    # path('account/', AccountView.as_view(), name='account')
]