from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Nauczyciel
from .serializers import NauczycielSerializer

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