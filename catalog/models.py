from django.db import models


# Create your models here.

class User(models.Model):
    tg_id = models.CharField(max_length=50)
    phone = models.IntegerField(null=True,
                                blank=True
                                )
    name = models.CharField(max_length=200,
                            null=True,
                            blank=True
                            )

    def __str__(self):
        return f'Клиент №{self.pk} {self.name}'


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ {self.pk}'
