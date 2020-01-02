from django.db import models


# Create your models here.
class Toko(models.Model):
    urltoko = models.CharField(max_length=1024, primary_key=True)
    nama_toko = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255, null=True, blank=True)
    ecommerce = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.nama_toko + " - " + self.ecommerce)

    class Meta:
        verbose_name_plural = "Toko"


class Produk(models.Model):
    urlproduk = models.CharField(max_length=1024, primary_key=True)
    toko = models.ForeignKey(Toko, on_delete=models.CASCADE)
    nama_produk = models.CharField(max_length=255)
    jumlah_terjual = models.IntegerField(default=0)
    jumlah_ulasan = models.IntegerField(default=0)
    kategori = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.nama_produk + " - " + self.toko.nama_toko)

    class Meta:
        verbose_name_plural = "Produk"


class Ulasan(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    nama_pengulas = models.CharField(max_length=255)
    variasi = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(default=1)
    tanggal = models.DateTimeField()
    ulasan = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.nama_pengulas + " - " + self.produk.nama_produk + " - " + self.produk.toko.nama_toko + " - " + self.tanggal.strftime('%B %d, %Y'))

    class Meta:
        verbose_name_plural = "Ulasan"

