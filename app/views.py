from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, mixins, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Movie, Theater, Showtime, Reservation
from .serializers import MovieSerializer, TheaterSerializer, ShowtimeSerializer, ReservationSerializer, RegisterSerializer

class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'director', 'genre']

class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        showtimes = instance.showtimes.all()
        showtime_serializer = ShowtimeSerializer(showtimes, many=True)
        data = serializer.data
        data['showtimes'] = showtime_serializer.data
        return Response(data)

class TheaterList(generics.ListCreateAPIView):
    queryset = Theater.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TheaterSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        if isinstance(data, dict):
            serializer = self.get_serializer(data=request.data)
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ShowtimeList(generics.ListCreateAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_time']
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        if isinstance(data, dict):
            serializer = self.get_serializer(data=request.data)
        if isinstance(data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        date_time = serializer.validated_data['date_time']
        if date_time < timezone.now():
            raise ValidationError("Showtime date and time must be in the future.")

        theater = serializer.validated_data['theater']
        theater = Theater.objects.get(pk=theater.id)
        available_seats = list(range(1, theater.capacity + 1))
        serializer.save(available_seats=available_seats)

@api_view(['GET'])
@permission_classes([AllowAny])
def available_seats(request, pk):
    showtime = Showtime.objects.get(pk=pk)
    reserved_seats = set().union(*showtime.reservations.values_list('reserved_seats', flat=True))
    available_seats = [seat for seat in showtime.available_seats if seat not in reserved_seats]
    return Response({'available_seats': available_seats})

@api_view(['POST'])
def reserve_seats(request, pk):
    showtime = Showtime.objects.get(pk=pk)
    seat_numbers = request.data.get('seats', [])
    
    if not seat_numbers:
        return Response({"error": "Seats must be provided."}, status=400)
    
    # Check if all seats are available

    available_seats = showtime.available_seats
    for seat in seat_numbers:
        if seat not in available_seats:
            return Response({"error": f"Seat {seat} is not available."}, status=400)

    user = request.user
    reservation = Reservation.objects.create(user=user, showtime=showtime, reserved_seats=seat_numbers)

    for seat in seat_numbers:
        available_seats.remove(seat)
    showtime.available_seats = available_seats
    showtime.save()

    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=201)

@api_view(['POST'])
def purchase_tickets(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    if reservation.user != request.user:
        return Response({"error": "You can only purchase tickets for your own reservations."}, status=403)

    reservation.is_purchased = True
    reservation.save()
    
    user_email = reservation.user.email
    subject = "Your tickets have been purchased successfully!"
    message = (
        f"Hello {reservation.user.username},\n\n"
        "Your tickets for the reservation ID "
        f"{reservation.pk} have been successfully purchased.\n\n"
        "Thank you for using our service!\n\n"
        "Best regards,\n"
        "Movie Ticket Booking Team"
    )
    
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [user_email], fail_silently=True)

    return Response({"message": "Tickets purchased successfully."}, status=200)

@api_view(['GET'])
def purchased_tickets(request):
    reservations = Reservation.objects.filter(user=request.user)
    reservations = reservations.filter(is_purchased=True)
    reservation_data = []
    for reservation in reservations:
        serializer = ReservationSerializer(reservation)
        reservation_data.append(serializer.data)
    return Response(reservation_data, status=200)

class ReservationList(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
class RegisterAPIVIew(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data =  data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            
            if User.objects.filter(username=username).exists():
                message = {
                    "message" : "Username already exists"
                }
                
                return Response(message,400)
            
            user = User.objects.create_user(username=username, password=password, email=email)
            
            refresh_token  = RefreshToken.for_user(user)
            
            message = {
                "message" : "Registration successful and Logging in",
                "token" : str(refresh_token.access_token)
            }
            
            return Response(message, 201)
            
        return Response(serializer.errors,400)
            
            
            
        