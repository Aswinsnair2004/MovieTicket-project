from movie_app.models import Movie
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Show 

@login_required
def home(request):
    movies = Movie.objects.all()  # ⛔ remove prefetch_related
    return render(request, 'authentication/home.html', {'movies': movies})
@login_required
def book_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    # Add booking logic here (e.g., save booking to the database)
    messages.success(request, f"You have successfully booked the show for {show.movie.title} at {show.show_time}.")
    return redirect('home')
@login_required
def booking_confirmation(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'authentication/booking_confirmation.html', {'show': show})