from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'przedmioty', views.PrzedmiotViewSet)
router.register(r'nauczyciele', views.NauczycielViewSet)
router.register(r'uczniowie', views.UczenViewSet)
router.register(r'opinie', views.OpiniaViewSet)
router.register(r'lekcje', views.LekcjaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
]