from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, InsumoViewSet, RecetaViewSet, VentaViewSet, MermaViewSet,
    login_view
    #RecetaInsumoViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'insumos', InsumoViewSet, basename='insumo')
router.register(r'recetas', RecetaViewSet, basename='receta')
router.register(r'ventas', VentaViewSet, basename='venta')
router.register(r'mermas', MermaViewSet, basename='merma')
# TODO: Resolver el issue de RecetaInsumoViewSet para dejarlo habilitado
#router.register(r'recetainsumos', RecetaInsumoViewSet, basename='recetainsumo')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
] 