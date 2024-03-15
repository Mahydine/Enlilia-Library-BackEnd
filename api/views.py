from django.shortcuts import render
from rest_framework import generics
from .models import Livre, Panier
from .serializers import LivreSerializer, PanierSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
import json
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


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
            return JsonResponse({'message': 'Utilisateur créé avec succès'}, status=201)
        else:
            return JsonResponse({'message': 'Cet utilisateur existe déjà'}, status=400)
    else:
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)

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

#Paniers :
    
class getAllPaniers(generics.ListCreateAPIView): #si on utilise GET dans la requette on récupère tous les livres, si c'est POST on insère un livre en bd
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPanier(request):
    user = request.user

    panier = get_object_or_404(Panier, utilisateur=user)
    livres = panier.livres.all()
    serializedLivres = LivreSerializer(livres, many=True).data

    return Response({'livres': serializedLivres})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AjouterLivreAuPanier(request):
    livre_id = request.data.get('livre_id')
    livre = get_object_or_404(Livre, id=livre_id)
    user = request.user

    panier, created = Panier.objects.get_or_create(utilisateur=user)

    if livre not in panier.livres.all():
        panier.livres.add(livre)
        return Response({'successMsg': 'Livre ajouté au panier avec succès'})
    else:
        return Response({'errorMsg': 'Le livre est déjà dans le panier'}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RetirerLivreDuPanier(request):
    livre_id = request.data.get('livre_id')
    livre = get_object_or_404(Livre, id=livre_id)
    user = request.user

    panier, created = Panier.objects.get_or_create(utilisateur=user)

    if livre in panier.livres.all():
        panier.livres.remove(livre)
        return Response({'message': 'Livre retiré du panier avec succès'})
    else:
        return Response({'message': 'Le livre n\'est pas dans le panier'}, status=400)
