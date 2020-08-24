"from django.db import models"
from djongo import models

class DatosMovimiento(models.Model):
    acc_x = models.DecimalField(max_digits=22, decimal_places=20)
    acc_y = models.DecimalField(max_digits=22, decimal_places=20)
    acc_z = models.DecimalField(max_digits=22, decimal_places=20)
    gyr_x = models.DecimalField(max_digits=22, decimal_places=20)
    gyr_y = models.DecimalField(max_digits=22, decimal_places=20)
    gyr_z = models.DecimalField(max_digits=22, decimal_places=20)
    fecha = models.CharField(max_length=25)
    hora = models.CharField(max_length=25)
    anomalia = models.BooleanField(default=False)
