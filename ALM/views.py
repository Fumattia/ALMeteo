from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from .postgres_database import *


# Create your views here.
def home(request):
    try:
        username = request.session['user']
        return render(request, 'ALM/home.html', {'username': username})
    except:
        return render(request, 'ALM/home.html')


def chi_siamo(request):
    try:
        username = request.session['user']
        return render(request, 'ALM/chi_siamo.html', {'username': username})
    except:
        return render(request, 'ALM/chi_siamo.html')

def il_nostro_servizio(request):
    try:
        username = request.session['user']
        return render(request, 'ALM/il_nostro_servizio.html', {'username': username})
    except:
        return render(request, 'ALM/il_nostro_servizio.html')

def sostienici(request):
    try:
        username = request.session['user']
        return render(request, 'ALM/sostienici.html', {'username': username})
    except:
        return render(request, 'ALM/sostienici.html')

def area_personale(request):
    username = request.session['user']
    username = username.upper()
    return render(request, 'ALM/area_personale.html', {'user': username})

def meteo_in_tempo_reale(request):
    prova = "ciao"
    temperatura = 20
    return render(request, 'ALM/meteo_in_tempo_reale.html', {'text': prova, 'temp': temperatura})

def user_login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            request.session['user'] = user
            login(request, user)
            # Success, now let's login the user.
            return home(request)
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'ALM/login.html',
                          {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data available, let's just show the page to the user.
        return render(request, 'ALM/login.html')

def logout(request):
    try:
        del request.session['user']
    except:
        return render(request, 'ALM/home.html')
    return render(request, 'ALM/home.html')

def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'ALM/register.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()

                # Login the user
                login(request, user)

                #create user on postgresql database
                conn = connect()
                nuovo_utente(conn, form.cleaned_data['username'], form.cleaned_data['password'], form.cleaned_data['first_name'], form.cleaned_data['last_name'], form.cleaned_data['email'], form.cleaned_data['phone_number'])
                close(conn)

                # redirect to accounts page:
                return user_login(request)

    # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})
