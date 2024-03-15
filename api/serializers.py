from rest_framework import serializers
from .models import Livre, Panier

#Sert à convertir les données d'un model en JSON pour pouvoir les transférer via l'API

class LivreSerializer(serializers.ModelSerializer):
    date_sortie = serializers.SerializerMethodField()

    def get_date_sortie(self, obj):
            return obj.date_sortie.strftime('%m-%Y')  # Formatage en "MM-AAAA"
    
    class Meta:
        model = Livre
        fields = ["id", "titre", "description", "auteur", "couverture", "prix", "date_sortie"]


class PanierSerializer(serializers.ModelSerializer):
    livres = LivreSerializer(many=True, read_only=True)

    class Meta:
        model = Panier
        fields = ["id", "utilisateur", "livres"]