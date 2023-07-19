from django.db import models


class Client(models.Model):
    """"""
    client_tg_id = models.IntegerField(verbose_name="ID пользователя")
    client_tg_username = models.CharField(max_length=200, verbose_name="Имя пользователя")

    def __str__(self):
        return self.client_tg_username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Order(models.Model):
    """"""
    client = models.ForeignKey(to='cake_app.Client', on_delete=models.CASCADE,
                               related_name="orders")
    address = models.TextField(verbose_name="Адресс заказа")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(verbose_name="Время доставки")
    promocode = models.CharField(max_length=50, blank=True, null=True,
                                 verbose_name="Промокод")
    is_active = models.BooleanField(blank=True, null=True, verbose_name="Готов ли заказ")
    comment = models.TimeField(blank=True, null=True, verbose_name="Комментарий к заказу")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
