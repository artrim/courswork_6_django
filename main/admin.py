from django.contrib import admin

from main.models import Mailing, Customer, Message, TryMailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('date', 'regularity', 'mailing_status', 'message',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'fio', 'comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body',)


@admin.register(TryMailing)
class TryMailingAdmin(admin.ModelAdmin):
    list_display = ('last_try_date', 'status', 'answer',)
