from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import BidderRegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.

def dashboard(request):
    # Render the dashboard template
    return render(request, 'dashboard/bac_dashboard.html')

def register_view(request):
    if request.method == 'POST':
        form = BidderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('bidder_dashboard')
    else:
        form = BidderRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            user = form.get_user()
            return redirect('bac_dashboard' if user.role == 'bac' else 'bidder_dashboard')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def bidder_dashboard(request):
    return render(request, 'dashboard/bidder_dashboard.html')

@login_required
def bac_dashboard(request):
    return render(request, 'dashboard/bac_dashboard.html')