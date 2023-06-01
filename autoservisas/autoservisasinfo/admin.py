from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models

# Register your models here.

class AutomobiliaiAdmin(admin.ModelAdmin):
    list_display = ('car', 'car_model')
    list_filter = ('car', 'car_model')
    fieldsets = (
        (_('General info'), {'fields': ('car', 'car_model')}),
    )


class KlientuAutomobiliaiAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_surname', 'car_model', 'car_number')
    list_filter = ('client_surname', 'car_model')
    fieldsets = (
        (_('Client info'), {'fields': ('client_name', 'client_surname')}),
        (_('Car info'), {'fields': ('car_model', 'car_number', 'vin_number')}),
    )
    search_fields = ('car_number', 'vin_number')


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('price', )
    fieldsets = (
        (_('Service info'), {'fields': ('name', 'price')}),
    )


class UzsakymoEiluteInline(admin.TabularInline):
    model = models.UzsakymoEilute
    can_delete = False
    extra = 0


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('order_date', 'car', 'price', 'status')
    list_filter = ('order_date', 'car')
    list_editable = ('status', )
    fieldsets = (
        (_('Order_info'), {'fields': ('order_date', 'price', 'car', 'status')}),
    )
    inlines = (UzsakymoEiluteInline, )

class UzsakymoEiluteAdmin(admin.ModelAdmin):
    list_display = ('paslauga', 'count','total_price', 'uzsakymas')
    list_filter = ('paslauga', )
    fieldsets = (
        (_('Uzsakymo eilute'), {'fields': ('paslauga', 'uzsakymas', 'count', 'total_price')}),
    )
    
    
admin.site.register(models.AutomobilioModelis, AutomobiliaiAdmin)
admin.site.register(models.Automobilis, KlientuAutomobiliaiAdmin)
admin.site.register(models.Uzsakymas, UzsakymasAdmin)
admin.site.register(models.Paslauga, PaslaugaAdmin)
admin.site.register(models.UzsakymoEilute, UzsakymoEiluteAdmin)