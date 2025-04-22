from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    poster = models.ImageField(upload_to='movie_posters/')

    def __str__(self):
        return self.title

class Show(models.Model):
    movie = models.ForeignKey(
        'Movie',
        on_delete=models.CASCADE,
        related_name='shows',
        default=1  # Replace 1 with the primary key of an existing Movie
    )
    show_time = models.DateTimeField()
    language = models.CharField(max_length=50)
    format = models.CharField(max_length=50)
    booked_seats = models.TextField(default="")  # Store booked seats as a comma-separated string

    def __str__(self):
        return f"{self.movie.title} - {self.show_time}"

class Ticket(models.Model):  # Correct indentation here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey('Show', on_delete=models.CASCADE)
    seats = models.TextField()  # Store selected seats as a comma-separated string
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket for {self.show.movie.title} - {self.user.username}"