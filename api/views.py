from django.shortcuts import render
from rest_framework import generics
from .models import Livre, Panier, LignePanier
from .serializers import LivreSerializer, PanierSerializer, LignePanierSerializer, UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework.views import APIView
import json
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import permissions


#Livres :

class getAndCreateLivres(generics.ListCreateAPIView): #si on utilise GET dans la requette on récupère tous les livres, si c'est POST on insère un livre en bd
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [AllowAny]

class GetDeleteOrUpdateLivre(generics.RetrieveUpdateDestroyAPIView): # GET => Récupère UN livre (selon l'id), PUT => met a jour UN livre, DELETE => supprime UN livre
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    lookup_field = "pk"

class LivreParTitre(generics.ListAPIView): #retourne une liste de tous les livres dont le titre contient le paramètre 'titre' passé dans l'URL. http://.../livres/recherche/?titre=MonTitre
    serializer_class = LivreSerializer

    def get_queryset(self): 

        queryset = Livre.objects.all()

        titre = self.request.query_params.get('titre', None)

        if titre is not None:
            queryset = queryset.filter(titre__icontains=titre)
        return queryset
    
# Authentification
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def isLogged(request):
    return JsonResponse({'logged': True})

@csrf_exempt
def inscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'successMsg': 'Utilisateur créé avec succès'}, status=201)
        else:
            return JsonResponse({'errorMsg': 'Cet utilisateur existe déjà'}, status=400)
    else:
        return JsonResponse({'errorMsg': 'Méthode non autorisée'}, status=405)

@api_view(['POST'])
def connexion(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Nom d\'utilisateur ou mot de passe incorrect'}, status=401)
    
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

#Paniers :
    
class getAllPaniers(generics.ListCreateAPIView): #si on utilise GET dans la requette on récupère tous les livres, si c'est POST on insère un livre en bd
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPanier(request):
    user = request.user
    panier = get_object_or_404(Panier, utilisateur=user)
    ligne_paniers = panier.ligne_paniers.all()  # Accès aux objets LignePanier liés au Panier
    serializedLignePaniers = LignePanierSerializer(ligne_paniers, many=True).data  # Vous aurez besoin de créer ce sérialiseur

    return Response({'livres': serializedLignePaniers})

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AjouterLivreAuPanier(request):
    livre_id = request.data.get('livre_id')
    livre = get_object_or_404(Livre, id=livre_id)
    user = request.user

    panier, _ = Panier.objects.get_or_create(utilisateur=user)
    ligne_panier, created = LignePanier.objects.get_or_create(panier=panier, livre=livre)

    if not created:
        ligne_panier.quantite += 1
        ligne_panier.save()

    return Response({'successMsg': 'Livre ajouté au panier avec succès'})

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RetirerLivreDuPanier(request):
    livre_id = request.data.get('livre_id')
    livre = get_object_or_404(Livre, id=livre_id)
    user = request.user

    panier, _ = Panier.objects.get_or_create(utilisateur=user)

    # Essayez de trouver la ligne du panier correspondant au livre à retirer
    try:
        ligne_panier = LignePanier.objects.get(panier=panier, livre=livre)
        ligne_panier.delete()  # Supprimez cette ligne du panier, retirant ainsi le livre peu importe la quantité
        return Response({'successMsg': 'Livre retiré du panier avec succès'})
    except LignePanier.DoesNotExist:
        return Response({'errorMsg': 'Le livre n\'est pas dans le panier'}, status=400)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AlreadyInPanier(request):
    livre_id = request.data.get('livre_id')
    user = request.user

    # Vérifiez si un Panier existe pour cet utilisateur et contient le livre spécifié.
    panier = Panier.objects.filter(utilisateur=user).first()
    
    if panier:
        # Utilisez le modèle LignePanier pour vérifier si le livre est déjà dans le panier.
        is_already_in_panier = LignePanier.objects.filter(panier=panier, livre__id=livre_id).exists()
    else:
        is_already_in_panier = False

    return Response({'alreadyInPanier': is_already_in_panier})