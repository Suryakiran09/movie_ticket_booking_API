from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    synopsis = models.TextField()

    def __str__(self):
        return self.title

class Theater(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='showtimes')
    date_time = models.DateTimeField()
    available_seats = models.JSONField(default=list)

    def __str__(self):
        return f"{self.movie.title} at {self.theater.name} on {self.date_time}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='reservations')
    reserved_seats = models.JSONField(default=list)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s reservation for {self.showtime}"