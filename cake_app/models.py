from django.db import models


class Client(models.Model):
    """Данные клиента (id и username в telegram)."""
    client_tg_id = models.IntegerField(verbose_name="ID пользователя")
    client_tg_username = models.CharField(max_length=200, verbose_name="Имя пользователя")

    def __str__(self):
        return self.client_tg_username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Order(models.Model):
    """Информация о заказе."""
    client = models.ForeignKey(to='cake_app.Client', on_delete=models.CASCADE,
                               related_name="orders", verbose_name="Клиент")
    readycake = models.ForeignKey(to='cake_app.ReadyCake', on_delete=models.SET_NULL, blank=True,
                                  null=True, verbose_name="Готовый торт",
                                  related_name="orders")
    customizedcake = models.ForeignKey(to='cake_app.CustomizedCake', on_delete=models.SET_NULL, blank=True,
                                       null=True, verbose_name="Торт, собранный самостоятельно",
                                       related_name="orders")
    address = models.TextField(verbose_name="Адресс заказа")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(verbose_name="Время доставки")
    promocode = models.CharField(max_length=50, blank=True, null=True,
                                 verbose_name="Промокод")
    is_active = models.BooleanField(blank=True, null=True, verbose_name="Готов ли заказ")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий к заказу")
    inscription = models.TextField(max_length=15, blank=True, null=True, verbose_name="Надпись на торте",
                                   help_text="Мы можем разместить на торте любую надпись, например: «С днем рождения!»")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class ReadyCake(models.Model):
    """Описание торта, уже имеющегося в ассортименте."""
    cake_name = models.CharField(max_length=200, verbose_name="Название торта")
    cake_price = models.IntegerField(verbose_name="Цена торта")
    cake_image = models.ImageField(upload_to="cake_image", verbose_name="Изображение торта")

    def __str__(self):
        return self.cake_name

    class Meta:
        verbose_name = "Готовый торт"
        verbose_name_plural = "Готовые торты"


class CustomizedCake(models.Model):
    """Информация о торте, который клиент собрал самостоятельно."""
    levels = models.IntegerField(verbose_name="Количество уровней торта")
    shape = models.CharField(max_length=20, verbose_name="Форма торта")
    filling = models.CharField(max_length=20, verbose_name="Начинка", default="Взбитые сливки")
    toping = models.CharField(max_length=30, verbose_name="Топпинг")
    berries = models.CharField(max_length=20, blank=True, null=True,
                               verbose_name="Ягоды")
    decore = models.CharField(max_length=30, blank=True, null=True,
                              verbose_name="Декор")

    class Meta:
        verbose_name = "Кастомизированный торт"
        verbose_name_plural = "Кастомизированные торты"
