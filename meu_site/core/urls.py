from django.contrib import admin
from django.urls import path,include
from .views import home,my_logout,cadastro
from django.contrib.auth import views as auth_views
from Perfil import urls as perfil_urls
urlpatterns = [
    path('',home,name="home"),
    path('cadastro/',cadastro,name="cadastro"),
    path('login/', auth_views.login, name = 'login'),
    path('logout/',my_logout, name = 'logout'),
    path('perfil/',include(perfil_urls)),
    
]

