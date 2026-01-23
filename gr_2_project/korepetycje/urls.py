from . import views
from django.urls import path

urlpatterns = [
    path('', views.lista_nauczycieli),
    path('<int:pk>/', views.nauczyciel),
    path('szukaj/<str:fragment>/', views.nauczyciel_szukaj),
    path('przedmiot/<str:przedmiot>/', views.nauczyciel_przedmiot),
]