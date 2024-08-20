# akun/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from akun import views
from django.contrib.auth.views import LoginView, LogoutView
from akun.views import profile_view, edit_profile_view
from .views import ProfileViewSet, profile_view, edit_profile_view, load_kabupaten, load_kecamatan, load_kelurahan

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    # URL API
    path('api/', include(router.urls)),  # Menggunakan 'api/' sebagai prefix untuk semua endpoint API

    # URL lainnya
    path('profile', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('ajax/load-kabupaten/', load_kabupaten, name='ajax_load_kabupaten'),
    path('ajax/load-kecamatan/', load_kecamatan, name='ajax_load_kecamatan'),
    path('ajax/load-kelurahan/', load_kelurahan, name='ajax_load_kelurahan'),
    path('weather/', views.weather_view, name='weather'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]