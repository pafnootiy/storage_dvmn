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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200,
                               null=True,
                               blank=True
                               )
    time = models.DateTimeField(auto_now=True)
    approx_size = models.IntegerField(null=False)
    comment = models.TextField(max_length=200,
                               null=True,
                               blank=True
                               )
    paid_till = models.DateTimeField(null=False)
    tariff = models.IntegerField(null=False)
    size = models.CharField(max_length=200,
                            null=True,
                            blank=True
                            )
    deleted = models.BooleanField()
    qr_code = models.CharField(max_length=200,
                               null=True,
                               blank=False)
    status = models.CharField(max_length=200,
                               null=True,
                               blank=True)

    def __str__(self):
        return f'Заказ {self.pk}'
