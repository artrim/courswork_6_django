from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="заголовок")
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(
        upload_to="blog/", verbose_name="превью", **NULLABLE,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания",)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Создан пользователем",
        **NULLABLE,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
