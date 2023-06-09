from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.car_list, name='cars'),
    path('available-cars/', views.available_cars, name='available_cars'),
    path('my-cars/', views.my_cars, name='my_cars'),
    path('assign_car/', views.assign_car, name='assign_car'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/my/', views.UserOrdersListView.as_view(), name='user_orders'),
    path('car/<int:pk>/order_reservation_form/', views.OrderReservationCreateView.as_view(), name='order_reservation_form'),
    path('order/<int:pk>/add_service/', views.AddServiceView.as_view(), name='add_service'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('car_update/<int:pk>/', views.CarUpdateView.as_view(), name='car_update'),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +  
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))