from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

def walidacja_daty_przyszlej(value):
    if value < timezone.now():
        raise ValidationError("Data lekcji nie może być w przeszłości!")

def walidacja_oceny(value):
    if value < 1 or value > 5:
        raise ValidationError("Ocena musi być w przedziale 1-5.")


class Przedmiot(models.Model):
    nazwa = models.CharField(max_length=100)
    opis = models.TextField(blank=True)

    class Meta:
        verbose_name = "Przedmiot"
        verbose_name_plural = "Przedmioty"

    def __str__(self):
        return self.nazwa

class Nauczyciel(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    numer_telefonu = models.CharField(max_length=20)
    przedmioty = models.ManyToManyField(Przedmiot)
    wlasciciel = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Nauczyciel"
        verbose_name_plural = "Nauczyciele"

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

class Uczen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    numer_telefonu = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Uczeń"
        verbose_name_plural = "Uczniowie"
        

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

class Lekcja(models.Model):
    data_odbywania = models.DateTimeField(validators=[walidacja_daty_przyszlej])
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

    def __str__(self):
        return f"{self.status}: {self.nauczyciel} - {self.uczen} ({self.data_odbywania})"
    
    class Meta:
        verbose_name = "Lekcja"
        verbose_name_plural = "Lekcje"
        ordering = ['data_odbywania']

class Opinia(models.Model):
    nauczyciel = models.ForeignKey(Nauczyciel, on_delete=models.CASCADE, related_name='opinie')
    uczen = models.ForeignKey(Uczen, on_delete=models.CASCADE)
    ocena = models.IntegerField(validators=[walidacja_oceny], help_text="Ocena od 1 do 5")
    komentarz = models.TextField()
    data_wystawienia = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Opinia"
        verbose_name_plural = "Opinie"

    def __str__(self):
        return f"Ocena {self.ocena} dla {self.nauczyciel}"