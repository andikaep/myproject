# accounts/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'tanggal_lahir', 'provinsi', 'kabupaten', 'kecamatan', 'kelurahan']
