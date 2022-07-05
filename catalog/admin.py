from django.contrib import admin
from catalog.models import User, Order, Tariff, Storage


# Register your models here.
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Tariff)
admin.site.register(Storage)