from django.db import models


# Create your models here.

class User(models.Model):
    tg_id = models.CharField(max_length=50)
    phone = models.IntegerField(null=True,
                                blank=True
                                )
    agreement = models.BooleanField(default=False)
    name = models.CharField(max_length=200,
                            null=True,
                            blank=True
                            )

    def __str__(self):
        return f'Клиент №{self.pk} {self.name}'



class Tariff(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    days = models.IntegerField()
    size = models.IntegerField()

    def __str__(self):
        return f'Тариф {self.title}'


class Storage(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200,
                               null=True,
                               blank=True
                               )
    comment = models.TextField(max_length=200,
                               null=True,
                               blank=True
                               )
    paid_till = models.DateTimeField(null=True)
    tariff = models.ForeignKey(Tariff, null=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=200,
                            null=True,
                            blank=True
                            )
    deleted = models.BooleanField(null=True)
    qr_code = models.CharField(max_length=200,
                               null=True,
                               blank=False)
    status = models.CharField(max_length=200,
                              null=True,
                              blank=True)
    storage = models.ForeignKey(Storage,
                                on_delete=models.CASCADE,
                                related_name='orders',
                                null=True)

    def __str__(self):
        return f'Заказ {self.pk}'



def get_db_tariff(tariff_id):
    tariff = Tariff.objects.get(pk=tariff_id)
    return tariff


def get_db_storage(storage_id):
    storage_id = Storage.objects.get(pk=storage_id)
    return storage


def create_db_user(update):
    user = User.objects.create(tg_id=update.message.chat.id)
    user.save()


def update_db_user(tg_id, phone=None, name=None, agreement=None):
    user = User.objects.get(tg_id=tg_id)
    if agreement:
        user.agreement = agreement
    if phone:
        user.phone = phone
    if name:
        user.name = name
    print(f'{user.tg_id} updated')
    user.save()


def create_db_order(update):
    user = User.objects.get(tg_id=update.message.chat.id)
    order = Order.objects.create(user=user)
    order.save()
    return order.id


def get_db_user(update):
    user = User.objects.get(tg_id=update.message.chat.id)
    return user


def update_db_order(id, address=None, tariff=None, paid_till=None,
                    comment=None, qr_code=None, status=None, deleted=None, storage=None):
    order = Order.objects.get(pk=id)
    if address:
        order.address = address
    if paid_till:
        order.paid_till = paid_till
    if comment:
        order.comment = comment
    if tariff:
        order.tariff = tariff
    if storage:
        order.storage = storage
    if qr_code:
        order.qr_code = qr_code
    if status:
        order.status = status
    if deleted:
        order.deleted = deleted
    print(f'{order.id} updated')
    order.save()

def check_if_agreement(update):
    return User.objects.filter(tg_id=update.message.chat.id).exists()
