from rest_framework import serializers
from .models import Livre, Panier, LignePanier, User

class LivreSerializer(serializers.ModelSerializer):
    date_sortie = serializers.SerializerMethodField()

    def get_date_sortie(self, obj):
            return obj.date_sortie.strftime('%m-%Y') 
    
    class Meta:
        model = Livre
        fields = ["id", "titre", "description", "auteur", "couverture", "prix", "date_sortie"]


class LignePanierSerializer(serializers.ModelSerializer):
    livre = LivreSerializer(read_only=True) 

    class Meta:
        model = LignePanier
        fields = ['livre', 'quantite']


class PanierSerializer(serializers.ModelSerializer):
    ligne_paniers = LignePanierSerializer(many=True, read_only=True)

    class Meta:
        model = Panier
        fields = ['id', 'utilisateur', 'ligne_paniers']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        # Incluez d'autres champs selon vos besoins