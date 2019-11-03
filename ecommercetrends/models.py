from django.db import models


# Create your models here.
class AbstractUlasan(models.Model):
    nama = models.TextField(null=True, blank=True)
    jenis = models.CharField(max_length=255, null=True, blank=True)
    rating = models.CharField(max_length=255, null=True, blank=True)
    tanggal = models.DateField()
    produk = models.CharField(max_length=255)
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.nama + " - " + self.produk + " - " + self.tanggal.strftime('%B %d, %Y'))

    class Meta:
        abstract = True


class SepatuPria(AbstractUlasan):
    pass

    class Meta:
        verbose_name_plural = 'Sepatu Pria'


class SepatuWanita(AbstractUlasan):
    pass

    class Meta:
        verbose_name_plural = 'Sepatu Wanita'
