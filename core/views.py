from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Pair, OtherConstraints
from core.forms import RequestPairForm, RequestGroupForm


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
        messages.info(request, 'You are already logged in, please logout to log in with another user!')
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

@login_required
def convalidation(request):
    if request.user.convalidationGranted:
        messages.error(request, 'Your grades have already been convalidated')
        return redirect(reverse('index'))
    # Get the grades needed
    theory = OtherConstraints.objects.all()[0].minGradeTheoryConv
    lab = OtherConstraints.objects.all()[0].minGradeLabConv
    # Check if requirements are met
    if  request.user.gradeTheoryLastYear >= theory \
        and request.user.gradeLabLastYear >= lab:
        request.user.convalidationGranted = True
        request.user.save()
        mensaje =   "Our team of teachers decided to convalidate your grades.\n This is because your\
                     theory grade was >= " + str(theory) + " and your lab grade was >= " + str(lab) + ". Congratulations!"
        messages.success(request, mensaje)
    else:
        mensaje =   "Our team of teachers decided to reject your convalidation request.\n This is because your\
                     theory grade was < " + str(theory) + " and / or your lab grade was < " + str(lab) + ". Congratulations!"
        messages.success(request, mensaje)
    # Go back to homepage
    return redirect(reverse('index'))


@login_required
def applypair(request):
    if request.method == 'POST':
        form = RequestPairForm(request.POST, user=request.user)

        if form.is_valid():
            return redirect(reverse('index'))
    else:
        form = RequestPairForm(user=request.user)
    return render(request, 'request_pair.html', {'form': form})



    



@login_required
def applygroup(request):
    if request.method == 'POST':
        form = RequestGroupForm(request.POST, user=request.user)

        if form.is_valid():
            return redirect(reverse('index'))
    else:
        form = RequestGroupForm(user=request.user)
    return render(request, 'request_group.html', {'form': form})