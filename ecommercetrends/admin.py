from django.contrib import admin
from .models import SepatuPria, SepatuWanita


# Register your models here.
class OrderDate(admin.ModelAdmin):
    date_hierarchy = 'tanggal'
    ordering = ('-tanggal',)
    list_display = ('nama', 'jenis', 'rating', 'produk', 'tanggal', 'review')


admin.site.register(SepatuPria, OrderDate)
admin.site.register(SepatuWanita, OrderDate)
