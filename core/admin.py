from django.contrib import admin

from .models import Machine, Color, Order

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create', 'active']
    ordering = ['-id']
    
    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create', 'active']
    ordering = ['id']
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', '_requester', 'personalization', 'color', 'machine', 'stage', 'finished', 'active']
    ordering = ['id']
    exclude = ['requester', ]
    list_filter = ['requester', 'stage', 'machine']
    list_editable = ['stage']

    def _requester(self, instance):
        return f'{instance.requester.get_full_name()}'
    
    def save_model(self, request, obj, form, change):
        obj.requester = request.user
        super().save_model(request, obj, form, change)
