from django.contrib import admin

# Register your models here.
# admin.py dans l'application 'cars'
from django.contrib import admin
from .models import Voiture, Marque, Reservation, Temoin

admin.site.register(Voiture)
admin.site.register(Marque)
admin.site.register(Reservation)
admin.site.register(Temoin)
