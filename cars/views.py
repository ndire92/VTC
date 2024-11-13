from django.shortcuts import redirect, render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Marque, Temoin, Voiture, Reservation
from .forms import FiltreVoitureForm, MarqueForm, ReservationForm, TemoinForm, VoitureForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Récupérer l'utilisateur et l'authentifier
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Se connecter avec l'utilisateur
                login(request, user)
                return redirect('dashboard')  # Redirige vers le dashboard après une connexion réussie
            else:
                # Authentification échouée
                return redirect('login')  # ou afficher un message d'erreur
    else:
        form = AuthenticationForm()

    return render(request, 'cars/login.html', {'form': form})

def liste_voitures(request):
    form = FiltreVoitureForm(request.GET)  # Récupère les critères de filtrage
    voitures = Voiture.objects.filter(disponibilite=True)  # Filtrer uniquement les voitures disponibles

    if form.is_valid():
        marque = form.cleaned_data.get('marque')
        annee = form.cleaned_data.get('annee')
        prix_par_jour = form.cleaned_data.get('prix_par_jour')
        carburant = form.cleaned_data.get('carburant')

        # Appliquer les filtres
        if marque:
            voitures = voitures.filter(marque=marque)
        if annee:
            voitures = voitures.filter(annee=annee)
        if prix_par_jour:
            voitures = voitures.filter(prix_par_jour=prix_par_jour)
        if carburant:
            voitures = voitures.filter(carburant=carburant)
    return render(request, 'cars/liste_voitures.html', {'form': form, 'voitures': voitures})


@login_required
def voiture_add(request):
    if request.method == 'POST':
        form = VoitureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('voiture_list')
    else:
        form = VoitureForm()
    return render(request, 'cars/voiture_form.html', {'form': form})

@login_required
def marque_list(request):
    marques = Marque.objects.all()
    return render(request, 'cars/marque_list.html', {'marques': marques})

@login_required
def marque_add(request):
    if request.method == 'POST':
        form = MarqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marque_list')
    else:
        form = MarqueForm()
    return render(request, 'cars/marque_form.html', {'form': form})


def voiture_details(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Assigner l'utilisateur seulement s'il est connecté
            if request.user.is_authenticated:
                reservation.utilisateur = request.user
                utilisateur_info = f"Utilisateur : {request.user.username}\n"
            else:
                utilisateur_info = ""  # Aucun utilisateur connecté

            reservation.voiture = voiture
            reservation.montant_total = voiture.prix_par_jour * (reservation.date_fin - reservation.date_debut).days
            reservation.save()

            # Créer le message WhatsApp
            message = (
                f"Nouvelle réservation :\n\n"
                f"Voiture : {voiture.marque.nom} {voiture.modele}\n"
                f"{utilisateur_info}"
                f"Date de début : {reservation.date_debut}\n"
                f"Date de fin : {reservation.date_fin}\n"
                f"Montant total : {reservation.montant_total} FCFA"
            )
            
            # Numéro WhatsApp
            whatsapp_number = '221775448536'
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message.replace(' ', '%20')}"

            # Rediriger vers le lien WhatsApp
            return redirect(whatsapp_url)
    else:
        form = ReservationForm()
    return render(request, 'cars/voiture_details.html', {'voiture': voiture, 'form': form})

def reservation_confirmation(request):
    return render(request, 'cars/reservation_confirmation.html')

@login_required
def dashboard(request):
    return render(request, 'cars/dashboard.html')

def reservation_list(request):
    reservations = Reservation.objects.all()
    # Ajoutez une logique conditionnelle ici pour préparer les noms des utilisateurs
    for reservation in reservations:
        if reservation.utilisateur is None:
            reservation.utilisateur_nom = "Utilisateur non connecté"
        else:
            reservation.utilisateur_nom = reservation.utilisateur.username
    return render(request, 'cars/reservation_list.html', {'reservations': reservations})

@login_required
def ajouter_temoin(request):
    if request.method == 'POST':
        form = TemoinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('temoin_list')  # Redirigez vers la liste des témoignages après l'ajout
    else:
        form = TemoinForm()
    return render(request, 'cars/ajouter_temoin.html', {'form': form})


def temoin_list(request):
    temoins = Temoin.objects.all()
    return render(request, 'cars/temoin_list.html', {'temoins': temoins})


def home(request):
    # Récupérer tous les témoignages
    temoins = Temoin.objects.all()

    # Récupérer les critères de filtrage
    form = FiltreVoitureForm(request.GET)
    
    # Récupérer les voitures disponibles
    voitures = Voiture.objects.filter(disponibilite=True)
    
    # Appliquer les filtres si le formulaire est valide
    if form.is_valid():
        marque = form.cleaned_data.get('marque')
        annee = form.cleaned_data.get('annee')
        prix_par_jour = form.cleaned_data.get('prix_par_jour')
        carburant = form.cleaned_data.get('carburant')

        # Appliquer les filtres sur les voitures
        if marque:
            voitures = voitures.filter(marque=marque)
        if annee:
            voitures = voitures.filter(annee=annee)
        if prix_par_jour:
            voitures = voitures.filter(prix_par_jour=prix_par_jour)
        if carburant:
            voitures = voitures.filter(carburant=carburant)

    # Paginater les voitures filtrées
    paginator = Paginator(voitures, 3)  # 9 voitures par page
    page_number = request.GET.get('page')
    voitures_paginated = paginator.get_page(page_number)
    
    # Passer les voitures paginées et les autres données au template
    return render(request, 'cars/home.html', {'voitures': voitures_paginated, 'temoins': temoins, 'form': form})
# Vue pour la page "À propos"
def about(request):
    return render(request, 'cars/about.html')

# Vue pour la page de contact
def contact(request):
    return render(request, 'cars/contact.html')