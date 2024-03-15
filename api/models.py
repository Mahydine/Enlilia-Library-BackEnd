from django.db import models
from django.contrib.auth import get_user_model

#Sert à crée les classes associées a la bd sqlite

class Livre (models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField(default="")
    auteur = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    couverture = models.URLField()
    date_sortie = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    

User = get_user_model()  # Récupère le modèle d'utilisateur de django


class Panier (models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paniers')
    livres = models.ManyToManyField(Livre, related_name='paniers')
    
    def __str__(self):
        return f"Panier de {self.utilisateur.username}"