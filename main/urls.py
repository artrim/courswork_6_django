from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, MessageListView, \
    MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, HomeTemplateView

app_name = MainConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('mailing_list', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('customer_list/', CustomerListView.as_view(), name='customer_list'),
    path('customer/<int:pk>/', cache_page(60)(CustomerDetailView.as_view()), name='customer_detail'),
    path('customer_create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customer_update/<int:pk>', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer_delete/<int:pk>', CustomerDeleteView.as_view(), name='customer_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='message_detail'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
]
