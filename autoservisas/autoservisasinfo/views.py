from typing import Any, Dict, Optional
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpResponse
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import generic
from django.db.models import Sum
from django.views.generic import CreateView
from . forms import OrderCommentForm, OrderReserveForm, ServiceForm
from . models import AutomobilioModelis, Automobilis, Uzsakymas, Paslauga, UzsakymoEilute
from django.views import View
from django.views.generic.edit import FormView
from django.shortcuts import redirect



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
    qs = Automobilis.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(car_model__car_model__icontains=query) |
            Q(car_model__car__icontains=query) 
        )
    else:
        qs = qs.filter(user__isnull=False)
    paginator = Paginator(qs, 6)
    car_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'autoservisas/cars.html', {
        'automobilis_list': car_list
    })

def available_cars(request):
    qs = Automobilis.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(car_model__car_model__icontains=query) |
            Q(car_model__car__icontains=query) 
        )
    else:
        qs = qs.filter(Q(user__isnull=True) | Q(user=None))  # Include cars without users
    paginator = Paginator(qs, 6)
    car_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'autoservisas/available_cars.html', {
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
                Q(car__user__username__icontains=query) |
                Q(car__car_number__icontains=query) |
                Q(car__car_model__car_model__icontains=query)
            )
        return qs

class OrderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'autoservisas/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.get_object()
        return context
    
    form_class = OrderCommentForm

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['commentator'] = self.request.user
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.order = self.get_object()
        form.instance.commentator = self.request.user
        form.save()
        messages.success(self.request, _('Comment added!'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('order_detail', kwargs={'pk':self.get_object().pk})

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
        orders = self.get_queryset()
        total_price = sum(order.price or 0 for order in orders)
        context['total_price'] = total_price
        return context


class OrderReservationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    form_class = OrderReserveForm
    template_name = 'autoservisas/order_reservation_form.html'
    success_url = reverse_lazy('user_orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = self.car
        return context

    def get_initial(self):
        car_id = self.kwargs['pk']
        self.car = get_object_or_404(Automobilis, pk=car_id)
        initial = super().get_initial()
        initial['car'] = self.car
        initial['order_date'] = date.today() + timedelta(days=14)
        initial['status'] = 0
        return initial

    def form_valid(self, form):
        form.instance.car = self.car
        form.instance.status = 0
        return super().form_valid(form)

class AddServiceView(FormView):
    form_class = ServiceForm
    template_name = 'autoservisas/add_service.html'
    success_url = reverse_lazy('autoservisas/user_orders')

    def form_valid(self, form):
        uzsakymas = get_object_or_404(Uzsakymas, pk=self.kwargs['pk'])
        service = form.cleaned_data['service']
        count = form.cleaned_data['count']
        total_price = service.price * count  # Calculate the sum based on the selected service and count

        uzsakymo_eilute = UzsakymoEilute.objects.create(uzsakymas=uzsakymas, paslauga=service, count=count, total_price=total_price)
        uzsakymas.status = 1
        uzsakymas.save()
        return redirect('order_detail', pk=uzsakymas.pk)