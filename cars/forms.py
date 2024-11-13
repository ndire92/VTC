# forms.py dans l'application 'cars'
from django import forms
from .models import Reservation, Temoin, Marque, Voiture
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
class MarqueForm(forms.ModelForm):
    class Meta:
        model = Marque
        fields = ['nom']

class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = ['marque', 'modele', 'annee', 'couleur', 'description', 'image', 'prix_par_jour', 'kilometrage', 'carburant', 'disponibilite']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['voiture', 'date_debut', 'date_fin', 'statut', 'montant_total']

    # Définir les widgets pour les champs Date
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'})
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'})
    )

class TemoinForm(forms.ModelForm):
    class Meta:
        model = Temoin
        fields = ['utilisateur', 'voiture', 'commentaire', 'note']
        
        


class FiltreVoitureForm(forms.Form):
    marque = forms.ModelChoiceField(queryset=Marque.objects.all(), required=False, label="Marque", empty_label="Choisir une marque")

    # Année : Choix des années disponibles dans la base de données
    annees_choices = [(annee, annee) for annee in Voiture.objects.values_list('annee', flat=True).distinct()]
    annee = forms.ChoiceField(choices=[('', 'Choisir une année')] + annees_choices, required=False, label="Année")

    # Prix : Choix des prix disponibles dans la base de données (ou une liste de prix prédéfinis)
    prix_choices = [(str(prix), f"{prix} FCFA") for prix in Voiture.objects.values_list('prix_par_jour', flat=True).distinct()]
    prix_par_jour = forms.ChoiceField(choices=[('', 'Choisir un prix')] + prix_choices, required=False, label="Prix par jour")

    # Carburant : Choix dynamique des carburants présents dans la base de données
    carburant_choices = [(carburant, carburant) for carburant in Voiture.objects.values_list('carburant', flat=True).distinct()]
    carburant = forms.ChoiceField(choices=[('', 'Choisir un carburant')] + carburant_choices, required=False, label="Carburant")