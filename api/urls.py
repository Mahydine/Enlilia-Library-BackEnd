from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # routes pour les livres
    path("livres/", views.getAndCreateLivres.as_view(), name="getAndCreateLivres"),
    path("livres/<int:pk>/", views.GetDeleteOrUpdateLivre.as_view(), name="GetDeleteOrUpdateLivre"),
    path('livres/recherche/', views.LivreParTitre.as_view(), name='livre-par-titre'),

    # routes pour les paniers
    path('panier/', views.getUserPanier, name='getUserPanier'),
    path('panier/ajouter/', views.AjouterLivreAuPanier, name='AjouterLivreAuPanier'),
    path('panier/retirer/', views.RetirerLivreDuPanier, name='RetirerLivreDuPanier'),

    # auth routes
    path('islogged/', views.isLogged, name='isLogged'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),

    #JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
