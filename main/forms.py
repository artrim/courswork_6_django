from django import forms

from main.models import Mailing, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('owner', 'date',)


class MailingModeratorForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('mailing_status',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)
