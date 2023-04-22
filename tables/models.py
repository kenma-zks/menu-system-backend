from django.db import models

# Create your models here.
class Table(models.Model):
    table_number = models.IntegerField(primary_key=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tables"

    def __str__(self):
        return str(self.table_number)