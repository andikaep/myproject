# akun/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    provinsi = models.CharField(max_length=50, blank=True)
    kabupaten = models.CharField(max_length=50, blank=True)
    kecamatan = models.CharField(max_length=50, blank=True)
    kelurahan = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username