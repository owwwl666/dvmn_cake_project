from django.contrib import admin
from .models import Client, Order


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["client_tg_id", "client_tg_username"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["address", "delivery_date", "delivery_time", "is_active"]
