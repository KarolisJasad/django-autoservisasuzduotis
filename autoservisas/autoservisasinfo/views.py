from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import generic
from django.db.models import Sum
from . models import AutomobilioModelis, Automobilis, Uzsakymas, Paslauga, UzsakymoEilute

# Create your views here.

def index(request):
    num_cars = AutomobilioModelis.objects.count()
    num_users = Automobilis.objects.count()
    num_services = Paslauga.objects.all().count()
    completed_orders = Uzsakymas.objects.filter(status__exact=2).count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_cars': num_cars,
        'num_users': num_users,
        'num_services': num_services,
        'completed_orders': completed_orders,
        'num_visits': num_visits,
    }

    return render(request, 'autoservisas/index.html', context)

def car_list(request):
    qs = AutomobilioModelis.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(car__istartswith=query) |
            Q(car_model__icontains=query)
        )
    else:
        qs = qs.all()
    paginator = Paginator(qs, 6)
    car_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'autoservisas/cars.html', {
        'automobilis_list': car_list
    })

def car_detail(request, pk):
    automobilis = get_object_or_404(Automobilis, pk=pk)
    automobilis_list = Automobilis.objects.filter(car_model=automobilis.car_model)
    return render(request, 'autoservisas/car_detail.html', {'automobilis': automobilis, 'automobilis_list': automobilis_list})


class OrderListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 6
    template_name = 'autoservisas/order_list.html'
    context_object_name = 'order_list'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(order_date__contains=query) |
                Q(car__client_name__icontains=query) |
                Q(car__client_surname__icontains=query) |
                Q(car__car_number__icontains=query) |
                Q(car__car_model__car_model__icontains=query)
            )
        return qs

class OrderDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'autoservisas/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_order = self.object
        related_orders = selected_order.uzsakymoEilutes.all()
        total_price = UzsakymoEilute.calculate_total_price(related_orders)
        context['total_price'] = total_price
        return context

class UserOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'autoservisas/user_orders.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(car__user=self.request.user).prefetch_related('uzsakymoEilutes')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uzsakymai = context['object_list']
        total_price = sum(uzsakymas.uzsakymoEilutes.aggregate(total_price=Sum('total_price')).get('total_price', 0) for uzsakymas in uzsakymai)
        context['total_price'] = total_price
        return context

