from rest_framework import serializers
from django.utils import timezone
from .models import Lekcja, Nauczyciel, Uczen

class LekcjaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    data_odbywania = serializers.DateTimeField(required=True)
    nauczyciel = serializers.PrimaryKeyRelatedField(queryset=Nauczyciel.objects.all())
    uczen = serializers.PrimaryKeyRelatedField(queryset=Uczen.objects.all())
    status = serializers.ChoiceField(choices=Lekcja.Status.choices, default=Lekcja.Status.PLANOWANA)

    def validate_data_odbywania(self,value):
        if value < timezone.now():
            raise serializers.ValidationError("Wybrana data jest niepoprawna")
        return value

    def create(self, validated_data):
        return Lekcja.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.data_odbywania = validated_data.get('data_odbywania', instance.data_odbywania)
        instance.nauczyciel = validated_data.get('nauczyciel', instance.nauczyciel)
        instance.uczen = validated_data.get('uczen', instance.uczen)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    

class NauczycielSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nauczyciel
        fields = ['imie','nazwisko','email','numer_telefonu','przedmioty']

class UczenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uczen
        fields = ['imie','nazwisko','email','numer_telefonu','przedmioty']

