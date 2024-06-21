import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse

from blog.models import Blog
from main.forms import MailingForm, MailingModeratorForm, MessageForm
from main.models import Mailing, Customer, Message
from main.services import get_mailing_from_cache, get_message_from_cache


class HomeTemplateView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        mailing_count = Message.objects.count()
        is_active_count = Mailing.objects.filter(mailing_status='started').count()
        customer_count = Customer.objects.distinct('email').count()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        random_blog_list = blog_list[:3]
        mailings = Mailing.objects.all()
        context_data = {
            'mailing_count': mailing_count,
            'is_active_count': is_active_count,
            'clients_count': customer_count,
            'random_blog_list': random_blog_list,
            'mailings': mailings,
        }
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        return get_mailing_from_cache()


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ('next_datetime', 'end_time', 'regularity', 'message', 'customers',)
    success_url = reverse_lazy('main:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('main:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        if user.has_perm('main.can_change_mailing_status'):
            return MailingModeratorForm
        raise PermissionDenied


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailing_list')


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    success_url = reverse_lazy('main:customer_list')
    fields = ('email', 'fio', 'comment',)

    def form_valid(self, form):
        customer = form.save()
        user = self.request.user
        customer.owner = user
        customer.save()

        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ('email', 'fio', 'comment',)

    def get_success_url(self):
        return reverse('main:customer_detail', args=[self.kwargs.get('pk')])


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('main:customer_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return get_message_from_cache()


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    success_url = reverse_lazy('main:message_list')
    fields = ('title', 'body',)

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MessageForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse('main:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')
