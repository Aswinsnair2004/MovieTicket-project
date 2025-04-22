from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from movie_app.models import Movie
from django.shortcuts import get_object_or_404
from movie_app.models import Movie, Show
from movie_app.models import Ticket
from django.core.paginator import Paginator
import logging
logger = logging.getLogger(__name__)

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        request.session["registration_success"] = True  
        return redirect("home")

    return render(request, "authentication/register.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "authentication/login.html")


@login_required
def dashboard(request):
    return render(request, "authentication/dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    movies = Movie.objects.prefetch_related('shows')
    return render(request, 'authentication/home.html', {'movies': movies})
@login_required
def book_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    # Add booking logic here (e.g., save booking to the database)
    messages.success(request, f"You have successfully booked the show for {show.movie.title} at {show.show_time}.")
    return redirect('home')
@login_required
def select_seats(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    booked_seats = show.booked_seats.split(",") if show.booked_seats else []
    seat_ids = [f"{row}{seat}" for row in "ABCDEF" for seat in range(1, 11)]
    
    if request.method == "POST":
        selected_seats = request.POST.getlist("seats")
        logger.debug(f"POST request received. Selected seats: {selected_seats}")
        if not selected_seats:
            messages.error(request, "Please select at least one seat.")
            return redirect('select_seats', show_id=show.id)

        # Pass selected seats to the payment page
        request.session['selected_seats'] = selected_seats
        request.session['show_id'] = show.id
        total_amount = len(selected_seats) * 200  # Example: ₹200 per seat
        request.session['total_amount'] = total_amount

        # Debug log before redirecting
        logger.debug(f"Redirecting to payment page with seats: {selected_seats}, total amount: {total_amount}")

        return redirect('payment_page')  # Redirect to the payment page

    logger.debug(f"GET request received. Rendering seat selection page.")
    return render(request, 'authentication/select_seats.html', {
        'show': show,
        'booked_seats': booked_seats,
        'seat_ids': seat_ids
    })
@login_required
def process_payment(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    if request.method == "POST":
        selected_seats = request.POST.getlist("seats")
        logger.debug(f"Processing payment for seats: {selected_seats}")  # Debugging here
        if not selected_seats:
            messages.error(request, "No seats selected for payment.")
            return redirect('select_seats', show_id=show.id)

        ticket = Ticket.objects.create(
            user=request.user,
            show=show,
            seats=",".join(selected_seats)
        )
        return render(request, 'movie_app/ticket.html', {
            'ticket': ticket,
            'show': show,
            'selected_seats': selected_seats
        })

    return redirect('home')
@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    logger.debug(f"Tickets for user {request.user}: {tickets}")
    return render(request, 'movie_app/my_tickets.html', {'tickets': tickets})
@login_required
def cancel_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        # Update the booked_seats field in the Show model
        booked_seats = ticket.show.booked_seats.split(",")
        canceled_seats = ticket.seats.split(",")
        updated_seats = [seat for seat in booked_seats if seat not in canceled_seats]
        ticket.show.booked_seats = ",".join(updated_seats)
        ticket.show.save()

        # Delete the ticket
        ticket.delete()
        messages.success(request, "Your ticket has been successfully canceled.")
        return redirect('my_tickets')

    return render(request, 'movie_app/cancel_ticket.html', {'ticket': ticket})
@login_required
def payment_page(request):
    selected_seats = request.session.get('selected_seats')
    show_id = request.session.get('show_id')
    total_amount = request.session.get('total_amount')

    logger.debug(f"Session data - Selected seats: {selected_seats}, Show ID: {show_id}, Total amount: {total_amount}")

    if not selected_seats or not show_id or not total_amount:
        messages.error(request, "Invalid payment session. Please select seats again.")
        return redirect('home')

    show = get_object_or_404(Show, id=show_id)

    if request.method == "POST":
        # Simulate payment processing
        payment_method = request.POST.get('payment_method')
        logger.debug(f"Payment method: {payment_method}")

        # Create a ticket after payment confirmation
        ticket = Ticket.objects.create(
            user=request.user,
            show=show,
            seats=",".join(selected_seats)
        )

        # Update booked seats in the Show model
        booked_seats = show.booked_seats.split(",") if show.booked_seats else []
        updated_booked_seats = booked_seats + selected_seats
        show.booked_seats = ",".join(updated_booked_seats)
        show.save()

        # Clear session data
        del request.session['selected_seats']
        del request.session['show_id']
        del request.session['total_amount']

        logger.debug(f"Ticket created successfully. Redirecting to ticket page.")
        return render(request, 'movie_app/ticket.html', {
            'ticket': ticket,
            'show': show,
            'selected_seats': selected_seats
        })

    # Debug log before rendering the payment page
    logger.debug(f"Rendering payment page for seats: {selected_seats}, total amount: {total_amount}")

    return render(request, 'movie_app/payment_page.html', {
        'show': show,
        'selected_seats': selected_seats,
        'total_amount': total_amount
    })