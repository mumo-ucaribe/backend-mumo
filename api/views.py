from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from django.contrib.auth.models import User
from .models import Insumo, Receta, Venta, Merma, RecetaInsumo
from .serializers import (
    UserSerializer, InsumoSerializer, RecetaSerializer,
    VentaSerializer, MermaSerializer, RecetaInsumoSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(detail=False, methods=['get'])
    def stock_bajo(self, request):
        """Retorna insumos con stock bajo (menos de 10 unidades)"""
        insumos = Insumo.objects.filter(cantidad__lt=10)
        serializer = self.get_serializer(insumos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def valor_total(self, request):
        """Calcula el valor total del inventario"""
        total = Insumo.objects.aggregate(
            valor_total=Sum(F('cantidad') * F('precio_unitario'))
        )
        return Response(total)

class RecetaViewSet(viewsets.ModelViewSet):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        insumos_data = request.data.pop('insumos', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(insumos=insumos_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        insumos_data = request.data.pop('insumos', [])
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(insumos=insumos_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Agrupa recetas por categoría"""
        categoria = request.query_params.get('categoria', None)
        if categoria:
            recetas = Receta.objects.filter(categoria=categoria)
        else:
            recetas = Receta.objects.all()
        serializer = self.get_serializer(recetas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def verificar_insumos(self, request, pk=None):
        """Verifica si hay suficientes insumos para preparar la receta"""
        receta = self.get_object()
        insumos_faltantes = []
        
        for receta_insumo in receta.recetainsumo_set.all():
            if receta_insumo.insumo.cantidad < receta_insumo.cantidad:
                insumos_faltantes.append({
                    'insumo': receta_insumo.insumo.nombre,
                    'cantidad_necesaria': receta_insumo.cantidad,
                    'cantidad_disponible': receta_insumo.insumo.cantidad
                })
        
        if insumos_faltantes:
            return Response({
                'status': 'error',
                'message': 'Faltan insumos',
                'insumos_faltantes': insumos_faltantes
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'status': 'success',
            'message': 'Hay suficientes insumos para preparar la receta'
        })

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(detail=False, methods=['get'])
    def ventas_por_periodo(self, request):
        """Obtiene ventas por período"""
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)
        
        ventas = self.queryset
        if fecha_inicio and fecha_fin:
            ventas = ventas.filter(fecha_venta__range=[fecha_inicio, fecha_fin])
        
        serializer = self.get_serializer(ventas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumen_ventas(self, request):
        """Obtiene un resumen de ventas"""
        total_ventas = self.queryset.filter(completada=True).count()
        ventas_pendientes = self.queryset.filter(completada=False).count()
        monto_total = self.queryset.filter(completada=True).aggregate(
            total=Sum('total')
        )['total'] or 0

        return Response({
            'total_ventas': total_ventas,
            'ventas_pendientes': ventas_pendientes,
            'monto_total': monto_total
        })

class MermaViewSet(viewsets.ModelViewSet):
    queryset = Merma.objects.all()
    serializer_class = MermaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(detail=False, methods=['get'])
    def mermas_por_periodo(self, request):
        """Obtiene mermas por período"""
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)
        
        mermas = self.queryset
        if fecha_inicio and fecha_fin:
            mermas = mermas.filter(fecha_merma__range=[fecha_inicio, fecha_fin])
        
        serializer = self.get_serializer(mermas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumen_mermas(self, request):
        """Obtiene un resumen de mermas por insumo"""
        resumen = self.queryset.values('insumo__nombre').annotate(
            total_merma=Sum('cantidad')
        ).order_by('-total_merma')
        
        return Response(resumen)

class RecetaInsumoViewSet(viewsets.ModelViewSet):
    queryset = RecetaInsumo.objects.all()
    serializer_class = RecetaInsumoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = RecetaInsumo.objects.all()
        receta_id = self.request.query_params.get('receta', None)
        if receta_id:
            queryset = queryset.filter(receta_id=receta_id)
        return queryset