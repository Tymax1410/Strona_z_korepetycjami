from django.contrib import admin
from .models import Lekcja, Nauczyciel, Uczen, Przedmiot, Opinia

class PrzedmiotAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "opis"]
    list_filter = ["nazwa"]

class LekcjaAdmin(admin.ModelAdmin):
    list_display = ["data_odbywania" , "nauczyciel" , "uczen", "status"]
    list_filter = ["data_odbywania"]

class NauczycielAdmin(admin.ModelAdmin):
    list_display = ["imie", "nazwisko", "email", "numer_telefonu", "get_przedmioty"]
    list_filter = ["nazwisko"]

    def get_przedmioty(self, obj):
        return ", ".join([p.nazwa for p in obj.przedmioty.all()])

class UczenAdmin(admin.ModelAdmin):
    list_display = ["imie", "nazwisko", "email", "numer_telefonu"]
    list_filter = ["nazwisko"]

    def get_przedmioty(self, obj):
        return ", ".join([p.nazwa for p in obj.przedmioty.all()])

admin.site.register(Przedmiot,PrzedmiotAdmin)
admin.site.register(Lekcja,LekcjaAdmin)
admin.site.register(Nauczyciel,NauczycielAdmin)
admin.site.register(Uczen,UczenAdmin)
admin.site.register(Opinia)