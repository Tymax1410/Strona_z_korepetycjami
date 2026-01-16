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
    numer_telefonu = models.CharField(max_length=20)
    przedmioty = models.ManyToManyField(Przedmiot)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Uczen(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    numer_telefonu = models.CharField(max_length=20)
    przedmioty = models.ManyToManyField(Przedmiot)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

class Lekcja(models.Model):
    data_odbywania = models.DateTimeField()
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.CASCADE)
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE)

    class Status(models.TextChoices):
        PLANOWANA = 'PL', 'Planowana'
        ODBYTA = 'ODB', 'Odbyta'
        ODWOLANA = 'ODW', 'Odwołana'
    
    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.PLANOWANA
    )