from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import NauczycielForm
from .models import Nauczyciel
from .serializers import NauczycielSerializer

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

@api_view(['GET', "POST"])
def lista_nauczycieli(request):
 
    if request.method == 'GET':
        nauczyciele = Nauczyciel.objects.all()
        serializer = NauczycielSerializer(nauczyciele, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = NauczycielSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def nauczyciel(request, pk):
    try:
        nauczyciel = Nauczyciel.objects.get(pk=pk)
    except Nauczyciel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NauczycielSerializer(nauczyciel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
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