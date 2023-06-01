from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from . models import AutomobilioModelis, Automobilis, Uzsakymas, Paslauga, UzsakymoEilute

# Create your views here.

def index(request):
    num_cars = AutomobilioModelis.objects.count()
    num_users = Automobilis.objects.count()
    num_services = Paslauga.objects.all().count()
    completed_orders = Uzsakymas.objects.filter(status__exact=2).count()

    context = {
        'num_cars': num_cars,
        'num_users': num_users,
        'num_services': num_services,
        'completed_orders': completed_orders,
    }

    return render(request, 'autoservisas/index.html', context)

def car_list(request):
    return render(request, 'autoservisas/cars.html', {
        'automobilis_list': AutomobilioModelis.objects.all()
    })

def car_detail(request, pk):
    automobilis = get_object_or_404(Automobilis, pk=pk)
    automobilis_list = Automobilis.objects.filter(car_model=automobilis.car_model)
    return render(request, 'autoservisas/car_detail.html', {'automobilis': automobilis, 'automobilis_list': automobilis_list})

class OrderListView(generic.ListView):
    model = Uzsakymas
    template_name = 'autoservisas/order_list.html'
    context_object_name = 'order_list'

class OrderDetailView(generic.DetailView):
    model = UzsakymoEilute
    template_name = 'autoservisas/order_detail.html'

