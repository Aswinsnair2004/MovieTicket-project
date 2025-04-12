from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
     path('book/<int:show_id>/', views.book_show, name='book_show'),
     path('select-seats/<int:show_id>/', views.select_seats, name='select_seats'),
     
]

if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)