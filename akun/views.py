# accounts/views.py
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm
from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer
from django.http import JsonResponse

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
@login_required
def profile_view(request):
    if request.method == 'POST':
        provinsi = request.POST.get('provinsi')
        kabupaten = request.POST.get('kabupaten')
        kecamatan = request.POST.get('kecamatan')
        kelurahan = request.POST.get('kelurahan')
        tanggal_lahir = request.POST.get('tanggal_lahir')

        profile = request.user.profile
        profile.provinsi = provinsi
        profile.kabupaten = kabupaten
        profile.kecamatan = kecamatan
        profile.kelurahan = kelurahan
        profile.tanggal_lahir = tanggal_lahir
        profile.save()
    provinsi_url = 'https://www.emsifa.com/api-wilayah-indonesia/api/provinces.json'
    response = requests.get(provinsi_url)
    provinsi_list = response.json() if response.status_code == 200 else []

    location = request.user.profile.location
    weather_data = None

    if location:
        api_key = '4282a26fb2726ce272aa7b1bc7d9e651' # Key API
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric&lang=id'

        try:
            response = requests.get(weather_url)
            if response.status_code == 200:
                weather_data = response.json()
                print(weather_data)
            else:
                print(f"Error: {response.status_code}")
                weather_data = None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            weather_data = None

    context = {
        'provinsi_list': provinsi_list,
        'location': location,
        'weather_data': weather_data,
    }
    return render(request, 'akun/profile.html', context)


@login_required
def edit_profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    provinsi_list = []
    kabupaten_list = []
    kecamatan_list = []
    kelurahan_list = []

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            provinsi = request.POST.get('provinsi')
            kabupaten_id = request.POST.get('kabupaten')
            kecamatan = request.POST.get('kecamatan')
            kelurahan = request.POST.get('kelurahan')
            tanggal_lahir = request.POST.get('tanggal_lahir')

            kabupaten_name = ""
            if kabupaten_id:
                api_url = f'https://www.emsifa.com/api-wilayah-indonesia/api/regencies/{provinsi}.json'
                response = requests.get(api_url)
                if response.status_code == 200:
                    kabupaten_data = response.json()
                    for kab in kabupaten_data:
                        if kab['id'] == kabupaten_id:
                            kabupaten_name = kab['name']
                            break

            profile.provinsi = provinsi
            profile.kabupaten = kabupaten_name
            profile.kecamatan = kecamatan
            profile.kelurahan = kelurahan
            profile.tanggal_lahir = tanggal_lahir
            profile.save()

            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

        # Load provinsi list
        provinsi_url = 'https://www.emsifa.com/api-wilayah-indonesia/api/provinces.json'
        response = requests.get(provinsi_url)
        provinsi_list = response.json() if response.status_code == 200 else []

        # Load kabupaten, kecamatan, kelurahan if they are already saved
        if profile.provinsi:
            kabupaten_url = f'https://www.emsifa.com/api-wilayah-indonesia/api/regencies/{profile.provinsi}.json'
            response = requests.get(kabupaten_url)
            kabupaten_list = response.json() if response.status_code == 200 else []

        if profile.kabupaten:
            kecamatan_url = f'https://www.emsifa.com/api-wilayah-indonesia/api/districts/{profile.kabupaten}.json'
            response = requests.get(kecamatan_url)
            kecamatan_list = response.json() if response.status_code == 200 else []

        if profile.kecamatan:
            kelurahan_url = f'https://www.emsifa.com/api-wilayah-indonesia/api/villages/{profile.kecamatan}.json'
            response = requests.get(kelurahan_url)
            kelurahan_list = response.json() if response.status_code == 200 else []

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'provinsi_list': provinsi_list,
        'kabupaten_list': kabupaten_list,
        'kecamatan_list': kecamatan_list,
        'kelurahan_list': kelurahan_list,
    }
    return render(request, 'akun/edit_profile.html', context)

def load_kabupaten(request):
    provinsi_id = request.GET.get('provinsi_id')
    api_url = f'https://www.emsifa.com/api-wilayah-indonesia/api/regencies/{provinsi_id}.json'
    response = requests.get(api_url)
    kabupaten_data = response.json()
    return JsonResponse(kabupaten_data, safe=False)

def load_kecamatan(request):
    kabupaten_id = request.GET.get('kabupaten_id')
    api_url = f'https://www.emsifa.com/api-wilayah-indonesia/api/districts/{kabupaten_id}.json'
    response = requests.get(api_url)
    kecamatan_data = response.json()
    return JsonResponse(kecamatan_data, safe=False)

def load_kelurahan(request):
    kecamatan_id = request.GET.get('kecamatan_id')
    api_url = f'https://www.emsifa.com/api-wilayah-indonesia/api/villages/{kecamatan_id}.json'
    response = requests.get(api_url)
    kelurahan_data = response.json()
    return JsonResponse(kelurahan_data, safe=False)

def home_view(request):
    return render(request, 'home.html')

def weather_view(request):
    location = request.user.profile.location
    weather_data = None

    if location:
        api_key = '4282a26fb2726ce272aa7b1bc7d9e651'  # Ganti dengan API key Anda yang valid
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric&lang=id'

        try:
            response = requests.get(weather_url)
            if response.status_code == 200:
                weather_data = response.json()
            else:
                weather_data = None
        except requests.exceptions.RequestException:
            weather_data = None

    context = {
        'location': location,
        'weather_data': weather_data,
    }
    return render(request, 'cuaca.html', context)