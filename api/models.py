from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Livre(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField(default="")
    auteur = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    couverture = models.URLField()
    date_sortie = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Panier(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paniers')

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"

class LignePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='ligne_paniers')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantite}x {self.livre.titre} dans le panier de {self.panier.utilisateur.username}"
