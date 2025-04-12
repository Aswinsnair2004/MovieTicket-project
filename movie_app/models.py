from django.db import models
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    poster = models.ImageField(upload_to='movie_posters/')

    def __str__(self):
        return self.title

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    show_time = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=50, default='English')
    format = models.CharField(max_length=20, default='2D')

    def __str__(self):
        return f"{self.movie.title} - {self.show_time}"
