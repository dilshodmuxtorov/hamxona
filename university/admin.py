from django.contrib import admin
from .models import UniversityModel, DormitoryModel, RoomModel, FurnitureModel


@admin.register(UniversityModel)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "longitude", "latitude", "phone_number")
    search_fields = ("name", "region", "phone_number")


@admin.register(DormitoryModel)
class DormitoryAdmin(admin.ModelAdmin):
    list_display = ("name", "university", "capacity")
    search_fields = ("name", "university__name")


@admin.register(RoomModel)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number", "floor", "capacity", "dormitory", "price")
    search_fields = ("number", "floor", "capacity", "dormitory__name")


@admin.register(FurnitureModel)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "room_id")
