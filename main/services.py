from django.core.cache import cache

from config.settings import CACHE_ENABLE

import smtplib
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

from config import settings
from main.models import Mailing, TryMailing, Message


def get_mailing_from_cache():
    if not CACHE_ENABLE:
        return Mailing.objects.all()
    key = 'mailing_list'
    mailing = cache.get(key)
    if mailing is not None:
        return mailing
    mailing = Mailing.objects.all()
    cache.set(key, mailing)
    return mailing


def get_message_from_cache():
    if not CACHE_ENABLE:
        return Message.objects.all()
    key = 'message_list'
    message = cache.get(key)
    if message is not None:
        return message
    message = Message.objects.all()
    cache.set(key, message)
    return message



def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_time = datetime.now(zone)

    # mailing_settings = Mailing.objects.filter(mailing_status__in=['create', 'started'])
    mailing_settings = Mailing.objects.filter(next_datetime__lte=current_time).filter(
        mailing_status__in=['create', 'started'])
    for mailing in mailing_settings:
        if mailing.next_datetime is None:
            mailing.next_datetime = current_time
        title = mailing.message.title
        body = mailing.message.body
        mailing.mailing_status = 'started'
        mailing.save()
        try:
            if mailing.end_time < mailing.next_datetime:
                mailing.next_datetime = current_time
                mailing.mailing_status = 'done'
                mailing.save()
                continue
            if mailing.next_datetime <= current_time:
                server_response = send_mail(
                    subject=title,
                    message=body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[customers.email for customers in mailing.customers.all()],
                    fail_silently=False,
                )
                if server_response == 1:
                    server_response = 'Сообщение отправлено'
                TryMailing.objects.create(status='success', answer=server_response, mailing=mailing)

                if mailing.regularity == 'daily':
                    mailing.next_datetime = current_time + timedelta(days=1)

                elif mailing.regularity == 'weekly':
                    mailing.next_datetime = current_time + timedelta(days=7)

                elif mailing.regularity == 'monthly':
                    mailing.next_datetime = current_time + relativedelta(months=1)

            mailing.save()

        except smtplib.SMTPException as error:
            TryMailing.objects.create(status='fail', answer=error, mailing=mailing)
