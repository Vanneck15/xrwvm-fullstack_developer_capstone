from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year']

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)