from django.db import models

# Modelo de Insumo
class Insumo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    

# Modelo de RecetaInsumo
class RecetaInsumo(models.Model):
    receta = models.ForeignKey('Receta', on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('receta', 'insumo')
    
    def save(self, *args, **kwargs):
        # Actualizar el precio unitario con el precio actual del insumo
        self.precio_unitario = self.insumo.precio_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.receta.nombre} - {self.insumo.nombre} ({self.cantidad} {self.insumo.unidad})"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

# Modelo de Receta
class Receta(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    insumos = models.ManyToManyField(Insumo, through=RecetaInsumo, related_name='recetas')
    descripcion = models.TextField()
    porciones = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def costo_total(self):
        return sum(item.subtotal for item in self.recetainsumo_set.all())

# Modelo de Venta
class Venta(models.Model):
    id = models.BigAutoField(primary_key=True)
    receta = models.ManyToManyField(Receta, related_name='ventas')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    completada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Venta {self.id} - Total: {self.total}"
    
class Merma(models.Model):
    id = models.BigAutoField(primary_key=True)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='mermas')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_merma = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Merma de {self.insumo.nombre} - Cantidad: {self.cantidad}"