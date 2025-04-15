from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/bidder/', views.bidder_dashboard, name='bidder_dashboard'),
    path('dashboard/bac/', views.bac_dashboard, name='bac_dashboard'),
]