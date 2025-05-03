
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class insumo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    

class receta(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    insumo = models.ManyToManyField(insumo, related_name='recetas')
    descripcion = models.TextField()
    porciones = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class venta(models.Model):
    id = models.BigAutoField(primary_key=True)
    receta = models.ManyToManyField(receta, related_name='ventas')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    completada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Venta {self.id} - Total: {self.total}"
    
class merma(models.Model):
    id = models.BigAutoField(primary_key=True)
    insumo = models.ForeignKey(insumo, on_delete=models.CASCADE, related_name='mermas')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_merma = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Merma de {self.insumo.nombre} - Cantidad: {self.cantidad}"