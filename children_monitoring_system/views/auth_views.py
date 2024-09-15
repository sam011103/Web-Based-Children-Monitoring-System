from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone
from ..models import User

@csrf_exempt
def loginIndex(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(1209600)  # Set session expiry to 2 weeks
                return JsonResponse({'redirect_url': '/home'})
            else:
                return JsonResponse({'errors': {'login_failed': ['The provided credentials do not match our records.']}}, status=401)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def registerIndex(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create and save the new user
            user = User(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password']),
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data['full_name'],  # Assuming using 'first_name' for full_name
                date_joined=timezone.now()
            )
            user.save()

            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def logoutIndex(request):
    logout(request)
    return redirect('login')

   