from django.urls import path
from .views import adiciona,mural,votos,perfil
urlpatterns = [
   
    path('adiciona/',adiciona,name="adiciona"),
    path('mural/',mural,name="mural"),
    path('votos/<int:user_id>/<int:info_id>/',votos,name="votos"),
    path('perfil/',perfil,name="perfil"),
]

