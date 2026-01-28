from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import CustomDjangoModelPermissions
from .forms import NauczycielForm
from .models import Nauczyciel, Przedmiot, Uczen, Lekcja, Opinia
from .serializers import NauczycielSerializer, PrzedmiotSerializer, UczenSerializer, LekcjaSerializer, OpiniaSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class PrzedmiotViewSet(viewsets.ModelViewSet):
    queryset = Przedmiot.objects.all()
    serializer_class = PrzedmiotSerializer
    permission_classes = [CustomDjangoModelPermissions]

class NauczycielViewSet(viewsets.ModelViewSet):
    queryset = Nauczyciel.objects.all()
    serializer_class = NauczycielSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get'])
    def szukaj(self, request):
        fragment = request.query_params.get('fragment', '')
        nauczyciele = Nauczyciel.objects.filter(nazwisko__startswith=fragment)
        serializer = self.get_serializer(nauczyciele, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def po_przedmiocie(self, request):
        nazwa_przedmiotu = request.query_params.get('nazwa', '')
        nauczyciele = Nauczyciel.objects.filter(przedmioty__nazwa=nazwa_przedmiotu)
        serializer = self.get_serializer(nauczyciele, many=True)
        return Response(serializer.data)

class UczenViewSet(viewsets.ModelViewSet):
    queryset = Uczen.objects.all()
    serializer_class = UczenSerializer
    permission_classes = [CustomDjangoModelPermissions]

class OpiniaViewSet(viewsets.ModelViewSet):
    queryset = Opinia.objects.none()
    serializer_class = OpiniaSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Opinia.objects.all()
            
        if hasattr(user, 'uczen'):
            return Opinia.objects.filter(uczen__user=user)

        if hasattr(user, 'nauczyciel_set'):
             return Opinia.objects.filter(nauczyciel__wlasciciel=user)
             
        return Opinia.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'uczen'):
            serializer.save(uczen=self.request.user.uczen)
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Tylko uczeń może wystawiać opinie.")

class LekcjaViewSet(viewsets.ModelViewSet):
    queryset = Lekcja.objects.none()
    serializer_class = LekcjaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Lekcja.objects.all()
        
        if hasattr(user, 'uczen'):
            return Lekcja.objects.filter(uczen__user=user)
            
        if hasattr(user, 'nauczyciel_set'):
             return Lekcja.objects.filter(nauczyciel__wlasciciel=user)

        return Lekcja.objects.none()
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'uczen'):
            serializer.save(uczen=self.request.user.uczen)
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Tylko użytkownik z profilem Ucznia może umawiać lekcje.")