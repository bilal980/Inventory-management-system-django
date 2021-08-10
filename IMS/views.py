from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.cache import cache
from django.contrib import messages
from django.urls import reverse_lazy
# from setting.models import BusinessDetail

def login_(request):
    # obj = BusinessDetail.objects.all().last().Name
    if request.method == 'POST':
        em = request.POST['email']
        pas = request.POST['password']
        user = authenticate(email=em, password=pas)
        if user is not None:
            login(request, user)
            if user.is_admin:
                messages.success(request, 'Welcome Admin!')
            else:
                messages.success(request, 'Welcome !')
            return redirect(reverse_lazy('dashboard'))
        messages.warning(request, "Invalid Login!")
    context = {'obj': 'obj'}
    return render(request, 'login.html', context)

def logout_(request):
    cache.clear()
    logout(request)
    return redirect('/')
