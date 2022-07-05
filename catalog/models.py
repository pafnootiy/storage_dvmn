from django.db import models
from geopy.distance import geodesic as GD


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
<<<<<<< Updated upstream
    lat = models.FloatField(max_length=30,
                            blank=False,
                            null=False)
    lon = models.FloatField(max_length=30,
                            blank=False,
                            null=False)
=======
>>>>>>> Stashed changes

    def __str__(self):
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200,
                               null=True,
                               blank=True
                               )
<<<<<<< HEAD
=======
    time = models.DateTimeField(auto_now=True)
    approx_size = models.IntegerField(null=False)
>>>>>>> main
    comment = models.TextField(max_length=200,
                               null=True,
                               blank=True
                               )
<<<<<<< HEAD
    paid_till = models.DateTimeField(null=True)
    tariff = models.ForeignKey(Tariff, null=True, on_delete=models.CASCADE)
=======
    paid_till = models.DateTimeField(null=False)
    tariff = models.IntegerField(null=False)
>>>>>>> main
    size = models.CharField(max_length=200,
                            null=True,
                            blank=True
                            )
<<<<<<< HEAD
    deleted = models.BooleanField(null=True)
=======
    deleted = models.BooleanField()
>>>>>>> main
    qr_code = models.CharField(max_length=200,
                               null=True,
                               blank=False)
    status = models.CharField(max_length=200,
<<<<<<< HEAD
                              null=True,
                              blank=True)
    storage = models.ForeignKey(Storage,
                                on_delete=models.CASCADE,
                                related_name='orders',
                                null=True)
=======
                               null=True,
                               blank=True)
>>>>>>> main

    def __str__(self):
        return f'Заказ {self.pk}'


def get_db_tariff(tariff_id):
    tariff = Tariff.objects.get(pk=tariff_id)
    return tariff


def get_db_storage(storage_id):
    storage_id = Storage.objects.get(pk=storage_id)
    return storage_id


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
<<<<<<< Updated upstream


def get_nearest_storage(location):
    storages = Storage.objects.all()
    print(storages)
    current_location = (location['latitude'], location['longitude'])
    result = {}
    for storage in storages:
        storage_id = storage.id
        storage_location = (storage.lat, storage.lon)
        distance = GD(current_location, storage_location).km
        result[storage_id] = distance
    print(result)
    min_distance = min(result.values())
    print(f'min_distance {min_distance}')
    for id, distance in result.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if distance == min_distance:
            print(id)
            return id
=======
>>>>>>> Stashed changes
