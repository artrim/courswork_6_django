from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}
FREQUENCY_CHOICES = [
    ("daily", "Раз в день"),
    ("weekly", "Раз в неделю"),
    ("monthly", "раз в месяц"),
]
STATUS_OF_NEWSLETTER = [
    ("create", "Создана"),
    ("started", "Запущена"),
    ("done", "Завершена"),
]
LOGS_STATUS_CHOICES = [
    ("success", "Успешно"),
    ("fail", "Не успешно"),
]


class Customer(models.Model):
    email = models.EmailField(verbose_name='почта', unique=True)
    fio = models.CharField(max_length=250, verbose_name='фио')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField(max_length=250, verbose_name='содержание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="начало рассылки")

    next_datetime = models.DateTimeField(verbose_name="следующая дата отправки", **NULLABLE)
    end_time = models.DateTimeField(verbose_name="конец рассылки", **NULLABLE)

    regularity = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, verbose_name='переодичность')
    mailing_status = models.CharField(max_length=50, choices=STATUS_OF_NEWSLETTER, default='create',
                                      verbose_name='статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="сообщение", related_name="mailing")
    customers = models.ManyToManyField(Customer, verbose_name='клиенты')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.date}, {self.regularity}, {self.message}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('can_change_mailing_status', 'Может отключать рассылку'),
        ]


class TryMailing(models.Model):
    last_try_date = models.DateTimeField(auto_now_add=True, verbose_name='дата последней попытки')
    status = models.CharField(max_length=50, choices=LOGS_STATUS_CHOICES, default='', verbose_name='статус')
    answer = models.TextField(verbose_name='ответ почтового сервера')
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="рассылка", **NULLABLE
    )
    client = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="клиент рассылки", **NULLABLE
    )

    def __str__(self):
        return f'{self.last_try_date}, \n{self.status}, \n{self.answer}'

    class Meta:
        verbose_name = 'попытка отправки'
        verbose_name_plural = 'попытки отправки'
