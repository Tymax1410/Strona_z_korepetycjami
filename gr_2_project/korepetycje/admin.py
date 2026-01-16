from django.contrib import admin
from .models import Lekcja

class LekcjaAdmin(admin.ModelAdmin):
    list_display = ["data_odbywania" , "nauczyciel" , "uczen", "status"]
    list_filter = ["data_odbywania"]

admin.site.register(Lekcja,LekcjaAdmin)