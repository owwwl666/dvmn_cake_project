from django.contrib import admin
from .models import Client, Order, ReadyCake, CustomizedCake, Baker


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["client_tg_id", "client_tg_username"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["client", "address", "delivery_date", "delivery_time", "is_active"]


@admin.register(ReadyCake)
class ReadyCake(admin.ModelAdmin):
    list_display = ["cake_name", "cake_price"]


@admin.register(CustomizedCake)
class CustomizedCakeAdmin(admin.ModelAdmin):
    list_display = ["levels", "shape", "toping", "filling", "berries", "decore"]


@admin.register(Baker)
class BakerAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "tg_username"]
