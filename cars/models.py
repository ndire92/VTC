from django.db import models

# Create your models# models.py dans l'application 'cars'
from django.db import models
from django.contrib.auth.models import User

# Modèle pour les marques de voiture
class Marque(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Modèle pour les voitures
class Voiture(models.Model):
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()
    couleur = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='voitures/')
    prix_par_jour = models.DecimalField(max_digits=10, decimal_places=2)
    kilometrage = models.IntegerField()
    carburant = models.CharField(max_length=50)
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marque.nom} {self.modele}"

# Modèle pour les réservations
class Reservation(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=50, choices=[('En attente', 'En attente'), ('Confirmée', 'Confirmée'), ('Annulée', 'Annulée')], default='En attente')
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)

def __str__(self):
    utilisateur_nom = self.utilisateur.username if self.utilisateur else "Utilisateur non connecté"
    return f"Réservation {self.id} pour {self.voiture.modele} - {utilisateur_nom}"





# Modèle pour les témoignages
class Temoin(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    commentaire = models.TextField()
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"Témoignage de {self.utilisateur.username} pour {self.voiture.modele}"
