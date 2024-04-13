from django.urls import path
from . import views
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Movie Ticket Booking API",
        default_version='v1',
        description="API for online movie ticket booking system",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('movies/', views.MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/', views.MovieDetail.as_view(), name='movie-detail'),
    path('theaters/', views.TheaterList.as_view(), name='theater-list'),
    path('showtimes/', views.ShowtimeList.as_view(), name='showtime-list'),
    path('showtimes/<int:pk>/available-seats/', views.available_seats, name='available-seats'),
    path('reservations/<int:pk>/reserve/', views.reserve_seats, name='reserve-seats'),
    path('reservations/', views.ReservationList.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/purchase/', views.purchase_tickets, name='purchase-tickets'),
    path('purchased_tickets/', views.purchased_tickets, name='purchased-seats'),
    path('accounts/login/', TokenObtainPairView.as_view() , name="login"),
    path('accounts/register/', views.RegisterAPIVIew.as_view(), name="register"),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]