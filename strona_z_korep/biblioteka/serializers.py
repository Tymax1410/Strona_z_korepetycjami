from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        # musimy wskazać klasę modelu
        model = Book
        # definiując poniższe pole możemy określić listę właściwości modelu,
        # które chcemy serializować
        fields = ['id', 'title', 'publication_month', 'book_format', 'author', 'genre', 'available_copies']
        # definicja pola modelu tylko do odczytu
        read_only_fields = ['id']