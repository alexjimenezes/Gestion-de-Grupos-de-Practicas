from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Pair


def index(request):
    context_dict = {}
    pairs = []
    if request.user.is_authenticated:
        try:
            pairs += Pair.objects.filter(student1=request.user.id)
        except:
            pass
        try:
            pairs += Pair.objects.filter(student2=request.user.id)
        except:
            pass
    
    context_dict['pairs'] = pairs

    return render(request, 'home.html', context=context_dict)


def user_login(request):
    # If user already logged in redirect to home page
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in, please logout to log in with another user!')
        return redirect(reverse('index'))
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                messages.error(request, 'The username or password are incorrect, please retry.')
                return render(request, 'login.html')

        # The request is not a HTTP POST, so display the login form.
        else:
            return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))