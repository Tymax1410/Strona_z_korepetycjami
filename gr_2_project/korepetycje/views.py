from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from .forms import NauczycielForm
from .models import Nauczyciel, Przedmiot
from .serializers import NauczycielSerializer

@login_required(login_url='/admin/login/')
def test_uprawnien_nauczyciela(request):
    nazwa_uprawnienia = 'korepetycje.can_view_other_owners'
    
    if request.user.has_perm(nazwa_uprawnienia):
        nauczyciele = Nauczyciel.objects.all()
        lista = ", ".join([n.imie for n in nauczyciele])
        return HttpResponse(f"Masz uprawnienie '{nazwa_uprawnienia}'.<br>Widzisz wszystkich: {lista}")
    
    else:
        return HttpResponse(f"BRAK uprawnienia '{nazwa_uprawnienia}'")

@login_required(login_url='/admin/login/')
def przedmiot_widok_dostepu(request, pk):
    if not request.user.has_perm('korepetycje.view_przedmiot'):
        raise PermissionDenied("Nie masz uprawnień do podglądania przedmiotów, przykro mi!")
    try:
        przedmiot = Przedmiot.objects.get(pk=pk)
        return HttpResponse(f"Masz uprawnienia. To jest przedmiot: {przedmiot.nazwa}")
    except Przedmiot.DoesNotExist:
        return HttpResponse(f"Masz uprawnienia, ale przedmiot o ID={pk} nie istnieje.")

def nauczyciel_delete_html(request,pk):
    nauczyciel = get_object_or_404(Nauczyciel, pk=pk)
    if request.method == 'POST':
        nauczyciel.delete()
        return redirect('nauczyciele_lista_html')
    else:
        return render(request, 'korepetycje/nauczyciel_potwierdz_usuwanie.html', {'nauczyciel': nauczyciel})

def nauczyciel_edit_html(request,pk):
    nauczyciel = get_object_or_404(Nauczyciel, pk=pk)
    if request.method == 'POST':
        form = NauczycielForm(request.POST, instance=nauczyciel)
        if form.is_valid():
            form.save()
            return redirect('nauczyciele_lista_html')
    else:
        form = NauczycielForm(instance=nauczyciel)
    return render(request, 'korepetycje/nauczyciel_form.html', {'form': form})


def nauczyciel_create_html(request):
    if request.method == 'POST':
        form = NauczycielForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nauczyciele_lista_html')
    else:
        form = NauczycielForm()
    return render(request, 'korepetycje/nauczyciel_form.html', {'form': form})

def nauczyciel_szczegoly_html(request, id):
    nauczyciel = get_object_or_404(Nauczyciel, pk=id) 
    return render(request, 'korepetycje/nauczyciel_szczegoly.html', {'nauczyciel': nauczyciel})

def nauczyciele_lista_html(request):
    nauczyciele = Nauczyciel.objects.all()
    return render(request, 'korepetycje/nauczyciele_lista.html', {'nauczyciele': nauczyciele})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def nauczyciele_dla_przedmiotu(request, pk):
    try:
        przedmiot = Przedmiot.objects.get(pk=pk)
    except Przedmiot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    nauczyciele = Nauczyciel.objects.filter(przedmioty=pk)
    serializer = NauczycielSerializer(nauczyciele, many=True)
    return Response(serializer.data)

@api_view(['GET', "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def lista_nauczycieli(request):
 
    if request.method == 'GET':
        nauczyciele = Nauczyciel.objects.filter(wlasciciel=request.user)
        serializer = NauczycielSerializer(nauczyciele, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = NauczycielSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciciel=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def nauczyciel_detail(request, pk):
    try:
        nauczyciel = Nauczyciel.objects.get(pk=pk, wlasciciel=request.user)
    except Nauczyciel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NauczycielSerializer(nauczyciel)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def nauczyciel_update_delete(request,pk):
    try:
        nauczyciel = Nauczyciel.objects.get(pk=pk, wlasciciel=request.user)
    except Nauczyciel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = NauczycielSerializer(nauczyciel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        nauczyciel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def nauczyciel_szukaj(request, fragment):
    nauczyciele = Nauczyciel.objects.filter(nazwisko__startswith=fragment)
    serializer = NauczycielSerializer(nauczyciele, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def nauczyciel_przedmiot(request,przedmiot):
    nauczyciele = Nauczyciel.objects.filter(przedmioty__nazwa=przedmiot)
    serializer = NauczycielSerializer(nauczyciele, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)