import base64
from rest_framework import serializers
from django.db import models
from .models import Unidades, Empleados, Imagen, Competencia, Roles, Empleados_roles

class UnidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidades
        fields = '__all__'

class EmpleadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleados
        fields = '__all__'

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = '__all__'

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class Empleados_unidadSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='componente.nombre_empleado', read_only=True)
    unidad_nombre = serializers.CharField(source='unidad.nombre_unidad', read_only=True)
    jefe_unidad = serializers.CharField(source='unidad.jefe_unidad', read_only=True)
    foto_empleado = serializers.CharField(source='id_imagen.foto', read_only=True)

    class Meta:
        model = Competencia
        fields = ['componente','empleado_nombre', 'unidad_nombre', 'jefe_unidad', 'foto_empleado']

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = ['componente2', 'valor', 'fecha']    

class Detalle_empleadoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='componente.nombre_empleado', read_only=True)
    empleado_email = serializers.EmailField(source='componente.email', read_only=True)
    promedio_valor = serializers.FloatField(read_only=True)
    foto_empleado = serializers.CharField(source='id_imagen.foto', read_only=True)
    competencias = CompetenciaSerializer(many=True, read_only=True)

    class Meta:
        model = Competencia
        fields = ['empleado_nombre','empleado_email', 'cargo', 'fortaleza','componente2','valor','promedio_valor','fecha','foto_empleado', 'competencias']

class competencia_unidadSerializer(serializers.ModelSerializer):
    promedio_competencias = serializers.SerializerMethodField()

    class Meta:
        model = Competencia
        fields = ['componente2', 'fecha', 'promedio_competencias']

    def get_promedio_competencias(self, obj):
        # Acceder a las competencias filtradas desde la vista
        view = self.context.get('view')
        if hasattr(view, 'competencias_filtradas'):
            competencias = view.competencias_filtradas.filter(componente2=obj.componente2)
            if competencias.exists():
                promedio = round(competencias.aggregate(models.Avg('valor'))['valor__avg'], 2)
                return promedio
        return 0


class resultado_empleados_unidad(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='componente.nombre_empleado', read_only=True)
    foto_empleado = serializers.CharField(source='id_imagen.foto', read_only=True)
    class Meta:
        model = Competencia
        fields = ['empleado_nombre', 'valor', 'foto_empleado']

class Resumen_equipoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='componente.nombre_empleado', read_only=True)
    foto_empleado = serializers.CharField(source='id_imagen.foto', read_only=True)

    class Meta:
        model = Competencia
        fields = ['empleado_nombre', 'cargo','valor', 'fecha','foto_empleado']

class Empleados_evaluadosSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='componente.nombre_empleado', read_only=True)
    unidad_nombre = serializers.CharField(source='unidad.nombre_unidad', read_only=True)
    foto_empleado = serializers.CharField(source='id_imagen.foto', read_only=True)

    class Meta:
        model = Competencia
        fields = ['evaluado','componente','empleado_nombre','unidad_nombre','foto_empleado']    

# Promedio de empleados
class EmpleadoSerializer(serializers.ModelSerializer):
    promedio_competencias = serializers.SerializerMethodField()
    nombre_unidad = serializers.SerializerMethodField()  # Agrega este campo

    class Meta:
        model = Empleados
        fields = ['codigo_empleado', 'nombre_empleado', 'promedio_competencias', 'nombre_unidad']

    def get_promedio_competencias(self, obj):
        competencias = Competencia.objects.filter(componente=obj)
        if competencias.exists():
            promedio = competencias.aggregate(models.Avg('valor'))['valor__avg']
            return promedio
        return 0

    def get_nombre_unidad(self, obj):
        # Obtener la unidad asociada al empleado
        try:
            unidad = obj.competencias.first().unidad.nombre_unidad
            return unidad
        except AttributeError:
            return None

#capacitandoce en el mes
class Capacitandoce_mesSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='componente.nombre_empleado', read_only=True)
    unidad_nombre = serializers.CharField(source='unidad.nombre_unidad', read_only=True)
    foto_empleado = serializers.CharField(source='id_imagen.foto', read_only=True)
    class Meta:
        model = Competencia
        fields = ['empleado_nombre', 'fecha_capacitacion', 'unidad_nombre', 'foto_empleado']

from rest_framework import serializers

class EmpleadoDetailSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    unidad = serializers.SerializerMethodField()
    foto = serializers.SerializerMethodField()

    class Meta:
        model = Empleados
        fields = ['codigo_empleado', 'email', 'nombre_empleado', 'unidad','foto', 'roles']

    def get_roles(self, obj):
        roles = Empleados_roles.objects.filter(id_empleado=obj)
        return [rol.id_rol.nombre_rol for rol in roles]
    
    def get_unidad(self, obj):
        try:
            unidad = obj.competencias.first().unidad.nombre_unidad
            return unidad
        except AttributeError:
            return None
    
    def get_foto(self, obj):
        # Suponiendo que hay una única imagen por empleado
        competencia = Competencia.objects.filter(componente = obj) # Obtener la primera competencia
        empleado = competencia.first()
        return empleado.id_imagen.foto if competencia and empleado.id_imagen else None