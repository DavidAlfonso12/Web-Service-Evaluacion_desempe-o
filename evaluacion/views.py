# myapp/views.py
from .serializer import UnidadesSerializer, EmpleadosSerializer, ImagenSerializer, Detalle_empleadoSerializer, Empleados_unidadSerializer, competencia_unidadSerializer, resultado_empleados_unidad, Empleados_evaluadosSerializer, CompetenciaSerializer, EmpleadoSerializer, Capacitandoce_mesSerializer,EmpleadoDetailSerializer
from django.db.models import Avg
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import models
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView
from .models import Unidades, Empleados, Imagen, Competencia
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from django.utils import timezone

class lista_unidades(viewsets.ModelViewSet):
    serializer_class = UnidadesSerializer

    def get_queryset(self):
        nombre_unidad = self.request.query_params.get('nombre_unidad', None)
        queryset = Unidades.objects.all()
        if nombre_unidad:
            queryset = queryset.filter(nombre_unidad = nombre_unidad)
        return queryset

class lista_empleados(viewsets.ModelViewSet):
    serializer_class = EmpleadosSerializer
    queryset = Empleados.objects.all()

class lista_imagenes(viewsets.ModelViewSet):
    serializer_class = ImagenSerializer
    queryset = Imagen.objects.all()

class lista_empleados_unidad(viewsets.ModelViewSet):
    serializer_class = Empleados_unidadSerializer

    def get_queryset(self):
        unidad_id = self.request.query_params.get('nombre_unidad', None)
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)

        # Convertir las fechas de string a objeto datetime
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio = timezone.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin = timezone.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except ValueError:
                # Manejar error de conversión
                return Competencia.objects.none()

        competencias = Competencia.objects.all()

        if unidad_id is not None:
            competencias = competencias.filter(unidad__nombre_unidad=unidad_id)

        if fecha_inicio and fecha_fin:
            competencias = competencias.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)

        seen_empleados = set()
        unique_competencias = []

        for competencia in competencias:
            empleado_nombre = competencia.componente.nombre_empleado
            if empleado_nombre not in seen_empleados:
                seen_empleados.add(empleado_nombre)
                unique_competencias.append(competencia)

        return unique_competencias


class Detalle_empleado(viewsets.ViewSet):
    def list(self, request):
        id_empleado = request.query_params.get('id_empleado', None)
        if id_empleado is not None:
            competencias = Competencia.objects.filter(componente__codigo_empleado=id_empleado)
            promedio_valor = competencias.aggregate(promedio=Avg('valor'))['promedio']

            competencias_data = []
            for competencia in competencias:
                competencias_data.append({
                    'componente2': competencia.componente2,
                    'valor': competencia.valor,
                    'fecha': competencia.fecha,
                })

            response_data = {
                'empleado_nombre': competencias.first().componente.nombre_empleado,
                'cargo': competencias.first().cargo,
                'email': competencias.first().componente.email,
                'fortaleza': competencias.first().fortaleza,
                'promedio_valor': promedio_valor,
                'foto_empleado': competencias.first().id_imagen.foto,
                'competencias': competencias_data,
            }
            return Response(response_data, status=200)

        return Response({'detail': 'Empleado no encontrado'}, status=404)

class competencias_unidad(viewsets.ModelViewSet):
    serializer_class = competencia_unidadSerializer

    def get_queryset(self):
        id_unidad = self.request.query_params.get('id_unidad', None)
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)

        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio = timezone.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin = timezone.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except ValueError:
                return Competencia.objects.none()

        if id_unidad is not None:
            # Filtra las competencias por ID de unidad
            competencias = Competencia.objects.filter(unidad__nombre_unidad=id_unidad)

            # Filtra por fechas si están presentes
            if fecha_inicio and fecha_fin:
                competencias = competencias.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)

            # Guardamos competencias filtradas en un atributo
            self.competencias_filtradas = competencias

            seen = set()
            unique_competencias = []
            for competencia in competencias:
                if competencia.componente2 not in seen:
                    seen.add(competencia.componente2)
                    unique_competencias.append(competencia)

            return unique_competencias
        
        return Competencia.objects.all()

    
class resultado_empleados_unidad(viewsets.ModelViewSet):
    serializer_class = resultado_empleados_unidad

    def get_queryset(self):
        nombre_unidad = self.request.query_params.get('nombre_unidad', None)
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)

        # Convertir las fechas de string a objeto datetime
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio = timezone.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin = timezone.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except ValueError:
                # Manejar error de conversión
                return Competencia.objects.none()

        competencias = Competencia.objects.all()

        if nombre_unidad is not None:
            competencias = competencias.filter(unidad__nombre_unidad=nombre_unidad)

        if fecha_inicio and fecha_fin:
            competencias = competencias.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)

        return competencias

class resumen_equipo(viewsets.ModelViewSet):
    serializer_class = Detalle_empleadoSerializer

    def get_queryset(self):
        nombre_unidad = self.request.query_params.get('nombre_unidad', None)
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)
        
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio = timezone.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin = timezone.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except ValueError:
                # Manejar error de conversión
                return Competencia.objects.none()
        
        if nombre_unidad is not None:
            competencias = Competencia.objects.filter(unidad__nombre_unidad=nombre_unidad)
            if fecha_inicio and fecha_fin:
                competencias = competencias.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)
            
            return competencias
        
        return Competencia.objects.all()

class Empleados_evaluados(viewsets.ModelViewSet):
    serializer_class = Empleados_evaluadosSerializer
    def get_queryset(self):
        evaluado = self.request.query_params.get('evaluado', None)
        if evaluado is not None:
            competencias = Competencia.objects.filter(evaluado=evaluado)
            seen = set()
            unique_competencias = []
            for competencia in competencias:
                if competencia.componente.nombre_empleado not in seen:
                    seen.add(competencia.componente.nombre_empleado)
                    unique_competencias.append(competencia)
            return unique_competencias
        return Competencia.objects.all()
    
class EmpleadosPromedioAPIView(viewsets.ViewSet):
    def list(self, request):
        empleados_con_promedio = []
        rango = self.request.query_params.get('rango', None)
        for empleado in Empleados.objects.all():
            promedio = empleado.competencias.aggregate(models.Avg('valor'))['valor__avg']
            if rango == '1':
                if promedio and promedio > 70:
                    empleados_con_promedio.append(empleado)
            else:
                if promedio and promedio < 70:
                    empleados_con_promedio.append(empleado)
        serializer = EmpleadoSerializer(empleados_con_promedio, many=True)
        return Response(serializer.data)
    
class MejoresCompetenciasViewSet(viewsets.ViewSet):
    def list(self, request):
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        competencias_mes = Competencia.objects.filter(fecha__month=5, fecha__year=anio_actual)

        promedios = (
            competencias_mes.values('componente2')
            .annotate(promedio=Avg('valor'))
            .order_by('-promedio')[:4]
        )

        return Response(promedios)
    
class CapacitandoceView(viewsets.ViewSet):
    def list(self, request):
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        capacitados = Competencia.objects.filter(
            capacitado=1,
            fecha_capacitacion__month=mes_actual,
            fecha_capacitacion__year=anio_actual
        )
        # Usar un conjunto para rastrear empleados y fechas ya vistos
        seen = set()
        filtered_capacitados = []
        for competencia in capacitados:
            key = (competencia.componente.nombre_empleado, competencia.fecha_capacitacion)
            if key not in seen:
                seen.add(key)
                filtered_capacitados.append(competencia)
        # Serializar los resultados filtrados
        serializer = Capacitandoce_mesSerializer(filtered_capacitados, many=True)
        return Response(serializer.data)
    
class LoginView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso a todos

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email y contraseña son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            empleado = Empleados.objects.get(email=email)
            if password == empleado.contrasena:
                serializer = EmpleadoDetailSerializer(empleado)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)
        except Empleados.DoesNotExist:
            return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_404_NOT_FOUND)