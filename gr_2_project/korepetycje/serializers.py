from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Przedmiot, Nauczyciel, Uczen, Lekcja, Opinia

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        Uczen.objects.create(user=user, imie=user.first_name, nazwisko=user.last_name, email=user.email, numer_telefonu="")
        return user

class PrzedmiotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Przedmiot
        fields = '__all__'

class NauczycielSerializer(serializers.ModelSerializer):
    przedmioty = serializers.StringRelatedField(many=True)
    class Meta:
        model = Nauczyciel
        fields = '__all__'

class UczenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uczen
        fields = '__all__'

class LekcjaSerializer(serializers.ModelSerializer):
    nauczyciel_str = serializers.CharField(source='nauczyciel', read_only=True)
    uczen_str = serializers.CharField(source='uczen', read_only=True)

    class Meta:
        model = Lekcja
        fields = ['id', 'data_odbywania', 'status', 'nauczyciel', 'uczen', 'nauczyciel_str', 'uczen_str']
        read_only_fields = ['status', 'uczen']

    def validate(self, data):
        nauczyciel = data['nauczyciel']
        data_lekcji = data['data_odbywania']
        zajety_termin = Lekcja.objects.filter(
            nauczyciel=nauczyciel, 
            data_odbywania=data_lekcji
        ).exclude(status='ODW').exists()

        if zajety_termin:
            raise serializers.ValidationError("Ten nauczyciel ma już zajęcia w tym terminie!")
            
        return data


class OpiniaSerializer(serializers.ModelSerializer):
    uczen_str = serializers.CharField(source='uczen', read_only=True)
    class Meta:
        model = Opinia
        fields = '__all__'
        read_only_fields = ['uczen', 'data_wystawienia']