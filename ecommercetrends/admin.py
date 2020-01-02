from django.contrib import admin
from .models import Ulasan, Toko, Produk


# Register your models here.
admin.site.register(Toko)
admin.site.register(Ulasan)
admin.site.register(Produk)
