from django.contrib import admin

from .models import Machine, Color, Order

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create', 'active']
    
    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create', 'active']
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'requester', 'personalization', 'color', 'stage', 'finished']
