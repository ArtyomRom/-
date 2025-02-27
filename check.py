from django.db import models

class Cake(models.Model):
    levels = models.IntegerField(choices=[
        (1, '1 уровень (+400 руб.)'),
        (2, '2 уровня (+750 руб.)'),
        (3, '3 уровня (+1100 руб.)')
    ], verbose_name='Количество уровней')

    shape = models.ForeignKey('Shape', on_delete=models.CASCADE, verbose_name="Форма торта")
    topping = models.ForeignKey('Topping', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Топинг')
    berries = models.ManyToManyField('Berry', blank=True, verbose_name='Ягоды')
    decor = models.ManyToManyField('Decor', blank=True, verbose_name='Декор')

    inscription = models.CharField(max_length=200, blank=True, null=True, verbose_name="Надпись (+500 руб.)")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")

    def save(self, *args, **kwargs):
        """Пересчет цены перед сохранением"""
        base_price = {1: 400, 2: 750, 3: 1100}[self.levels]
        shape_price = self.shape.price
        topping_price = self.topping.price if self.topping else 0
        berries_price = sum(berry.price for berry in self.berries.all())
        decor_price = sum(decor.price for decor in self.decor.all())
        inscription_price = 500 if self.inscription else 0

        self.price = base_price + shape_price + topping_price + berries_price + decor_price + inscription_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Торт {self.shape} ({self.levels} уровня) - {self.price} руб."


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заказчик')
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, verbose_name="Торт")
    address = models.TextField(verbose_name="Адрес доставки")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(verbose_name="Время доставки")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая цена")
    created_at = models.DateTimeField(auto_now_add=True)
