from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.lista_nauczycieli),
    path('<int:pk>/', views.nauczyciel),
    path('szukaj/<str:fragment>/', views.nauczyciel_szukaj),
    path('przedmiot/<str:przedmiot>/', views.nauczyciel_przedmiot),
    path('html/', views.nauczyciele_lista_html, name='nauczyciele_lista_html'),
    path('html/<int:id>/', views.nauczyciel_szczegoly_html, name='nauczyciel_szczegoly_html'),
    path('html/stworz_nauczyciela/', views.nauczyciel_create_html, name='nauczyciel_form_html'),
    path('html/edytuj_nauczyciela/<int:pk>/', views.nauczyciel_edit_html, name='nauczyciel_edit_html'),
    path('html/usun_nauczyciela/<int:pk>/', views.nauczyciel_delete_html, name='nauczyciel_delete_html'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]