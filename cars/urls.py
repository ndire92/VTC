# urls.py dans l'application 'cars'
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('voitures/', views.liste_voitures, name='liste_voitures'),
    path('voiture/<int:voiture_id>/', views.voiture_details, name='voiture_details'),
    path('reservation/confirmation/', views.reservation_confirmation, name='reservation_confirmation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reservations/', views.reservation_list, name='reservation_list'),  # Vérifiez que ce nom existe
    path('temoins/', views.temoin_list, name='temoin_list'),  # Assurez-vous que ce nom existe
    path('temoin/ajouter/', views.ajouter_temoin, name='ajouter_temoin'),
    path('voitures/add/', views.voiture_add, name='voiture_add'),
    path('marques/', views.marque_list, name='marque_list'),
    path('marques/add/', views.marque_add, name='marque_add'),
    path('', views.home, name='home'),  # Page d'accueil
    path('about/', views.about, name='about'),  # Page à propos
    path('contact/', views.contact, name='contact'),  # Page de contact
        # Ajoutez ces deux lignes pour gérer la connexion et la déconnexion
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   






]
