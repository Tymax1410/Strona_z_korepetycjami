from django.db import models

class Przedmiot(models.Model):
    nazwa = models.CharField(max_length=100)
    opis = models.TextField(blank=True)

    def __str__(self):
        return self.nazwa

class Nauczyciel(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    przedmioty = models.ManyToManyField(Przedmiot)

class Lekcja(models.Model):
    data_odbywania = models.DateField()
    prowadzacy = models.ManyToManyField(Nauczyciel)
    uczniowie = 
