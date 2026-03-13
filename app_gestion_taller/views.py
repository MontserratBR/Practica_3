from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Cliente, Coche, Servicio, CocheServicio

# Funcion para regitrar un cliente en la base de datos, recibe un JSON con los
# datos del cliente y devuelve un mensaje de éxito o error.
@csrf_exempt
def registrar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data['nombre'],
                telefono=data['telefono'],
                email=data['email']
            )
            return JsonResponse({"mensaje": "Cliente registrado con éxito", "cliente_id": cliente.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

#Funcion para registrar un coche en la base de datos, recibe un JSON con los datos
# del coche y el id del cliente al que pertenece, devuelve un mensaje de éxito o error.
@csrf_exempt
def registrar_coche(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=data['cliente_id'])
            coche = Coche.objects.create(
                cliente=cliente,
                marca=data['marca'],
                modelo=data['modelo'],
                matricula=data['matricula']
            )
            return JsonResponse({"mensaje": "Coche registrado con éxito", "coche_id": coche.id})
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

#Funcion para registrar un servicio en la base de datos, recibe un JSON con los datos del servicio
#y el id del coche al que se le va a realizar el servicio, devuelve un mensaje de éxito o error.
@csrf_exempt
def registrar_servicio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=data['coche_id'])
            servicio = Servicio.objects.create(
                nombre=data['nombre'],
                descripcion=data['descripcion']
            )
            CocheServicio.objects.create(coche=coche, servicio=servicio)
            return JsonResponse({"mensaje": "Servicio registrado con éxito", "servicio_id": servicio.id})
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

# Búsqueda de cliente por nombre 
@csrf_exempt
def buscar_cliente(request, cliente_nombre):
    try:
        cliente = Cliente.objects.values('id','telefono', 'email').get(nombre=cliente_nombre)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "EL cliente no fue encontrado"}, status=404)

#Listado de todos los clientes 
@csrf_exempt
def all_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_gestion_taller/all_clientes.html', {'clientes': clientes})

#Listado de coches
@csrf_exempt
def all_coches(request):
    coches = list(Coche.objects.values())
    return JsonResponse(coches, safe=False)
#Listado se servicios
@csrf_exempt
def all_servicios(request):
    servicios = list(Servicio.objects.values())
    return JsonResponse(servicios, safe=False)

#Filtrar coches por su modelo
@csrf_exempt
def filtrar_coche(request, modelo):
    coches = Coche.objects.values(
        'id', 'marca', 'modelo', 'matricula', 'cliente__nombre'
    ).filter(modelo=modelo)

    if not coches:
        return JsonResponse({"error": "No se encontraron coches"}, status=404)

    return JsonResponse(list(coches), safe=False)

#Muestra los servicos y coches que tiene un cliente, recibe el nombre del cliente.
@csrf_exempt
def servicios_cliente(request, cliente_nombre):
    try:
        cliente = Cliente.objects.get(nombre=cliente_nombre)
        coches = Coche.objects.filter(cliente=cliente)
        servicios = Servicio.objects.filter(coches__in=coches).distinct()
        contexto = {
            'cliente': cliente,
            'coches': coches,
            'servicios': servicios
        }
        return render(request, 'app_gestion_taller/servicios_coches.html', contexto)

    except Cliente.DoesNotExist:
        return JsonResponse({"error": "EL cliente no fue encontrado"}, status=404)
    

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    coches = Coche.objects.filter(cliente_id=cliente.id)

    if not coches.exists():
        mensaje = "Este cliente no tiene coches registrados."
    else:
        mensaje = None

    contexto = {
        'cliente': cliente,
        'coches': coches,
        'mensaje': mensaje
    }

    return render(request, 'app_gestion_taller/detalle_cliente.html', contexto)