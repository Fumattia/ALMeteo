from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import RegisterForm, StoricoForm
from .mysql_database import *
from .funzioni import *



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
    try:
        username = request.session['user']
        username = username.upper()
        print(username)
        return render(request, 'ALM/area_personale.html', {'username': username})
    except:
        return render(request, 'ALM/login.html')

def meteo_in_tempo_reale(request):

    try:
        username = request.session['user']
        conn = connect()
        id = seleziona_dato(conn, "Utenti", "ID_utente", "Username", username)
        id = id[0][0]
        codice = seleziona_dato(conn, "Stazioni", "Codice_stazione", "Id_utente", str(id))
        codice_stazione = codice[0][0]
        dati = seleziona_mirata(conn, "Dati", "codice_stazione", codice_stazione, 1)
        print(dati)
        print(codice_stazione)
        localita = seleziona_dato(conn, "Stazioni", "Posizione", "Codice_stazione", codice_stazione)
        print(localita)
        localita = localita[0][0].title()
        close(conn)

        temperatura = dati[0][1]
        umidita = dati[0][3]
        t_perc = dati[0][4]
        pres = dati[0][5]

        altitudine = dati[0][6]
        data = dati[0][10]
        ora = dati[0][11]

        return render(request, 'ALM/meteo_in_tempo_reale.html', {'text': localita, 'temp': temperatura, 'hum': umidita, 't_perc': t_perc, 'pres': pres, 'alt': altitudine, 'date': data, 'time': ora, 'username': username})
    except:
        try:
            username = request.session['user']
            conn = connect()
            id = seleziona_dato(conn, "Utenti", "ID_utente", "Username", username)
            id = id[0][0]
            pos = seleziona_dato(conn, "Stazioni", "Posizione", "Id_utente", str(id))
            localita = pos[0][0]
            return render(request, 'ALM/meteo_in_tempo_reale.html', {'username': username, 'text': localita})
        except:
            try:
                username = request.session['user']
                return render(request, 'ALM/meteo_in_tempo_reale.html', {'username': username})
            except:
                return render(request, 'ALM/home.html')


def storico_dati(request):

    template = 'ALM/storico_dei_dati.html'
    username = request.session['user']
    conn = connect()

    if request.method == 'POST':
        form = StoricoForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data['data']
            ora = form.cleaned_data['ora']
            luogo = form.cleaned_data['luogo'],

            if data == None and ora == '' and luogo == '':
                dati = seleziona(conn, "Dati", 100)
                return render(request, 'ALM/storico_dei_dati.html', {'form': form, 'username': username, 'dati': dati})
            dati = seleziona_mirata(conn, "Dati", "Data", data, 100)

            return render(request, template, {'form': form, 'username': username, 'dati': dati})
        else:
            dati = seleziona(conn, "Dati", 100)
            return render(request, 'ALM/storico_dei_dati.html', {'form': form, 'username': username, 'dati': dati})
    else:
        form = StoricoForm()
        dati = seleziona(conn, "Dati", 100)

        return render(request, 'ALM/storico_dei_dati.html', {'form': form, 'username': username, 'dati': dati})



def previsioni(request):
    try:
        username = request.session['user']
        return render(request, 'ALM/previsioni.html', {'username': username})
    except:
        return render(request, 'ALM/previsioni.html')

def gestione_account(request):
    try:
        username = request.session['user']
        username = username.upper()
        return render(request, 'ALM/gestisci_account.html', {'username': username})
    except:
        return render(request, 'ALM/gestisci_account.html')

def connessione_stazione(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        posizione = request.POST['posizione']
        codice_stazione = request.POST['codice']


        try:
            username = request.session['user']
            conn = connect()
            id = seleziona_dato(conn, "Utenti", "ID_utente", "Username", username)
            id = id[0][0]
            print(id)
            nuova_stazione(conn, posizione, id, codice_stazione)
            close(conn)
            return render(request, 'ALM/il_nostro_servizio.html', {'username': username})
        except:
            username = request.session['user']
            return render(request, 'ALM/connessione_stazione.html',
                          {'error_message': 'Connessione fallita', 'username': username})
    else:
        # No post data available, let's just show the page to the user.
        username = request.session['user']
        return render(request, 'ALM/connessione_stazione.html', {'username': username})



def user_login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        # user = authenticate(username=username, password=password)
        user = logga(request, username, password)
        print(user)
        if user is not None:
            # Save session as cookie to login the user
            request.session['user'] = username
            # login(request, user)
            # Success, now let's login the user.
            return home(request)
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'ALM/login.html',
                          {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data available, let's just show the page to the user.
        return render(request, 'ALM/login.html')

def recupera_password(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        # Check username and password combination if correct
        # user = authenticate(username=username, password=password)

        if User.objects.filter(username=username).exists():
            # Save session as cookie to login the user
            codice, mail = sendcodice(username)
            request.session['user'] = username
            request.session['cacca'] = codice
            request.session['mail'] = mail

            # login(request, user)
            # Success, now let's login the user.
            return render(request, 'ALM/inserisci_codice.html', {'mail': mail})
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'ALM/recupera_password.html',
                          {'error_message': 'Username non esistente'})
    else:
        # No post data available, let's just show the page to the user.
        return render(request, 'ALM/recupera_password.html')

def inserisci_codice(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        codice = request.POST['codice']
        # Check username and password combination if correct
        # user = authenticate(username=username, password=password)

        if codice == request.session['cacca']:

            return render(request, 'ALM/cambia_password.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            mail = request.session['mail']
            return render(request, 'ALM/inserisci_codice.html',
                          {'error_message': 'Codice non corretto', 'mail': mail})
    else:
        # No post data available, let's just show the page to the user.
        return render(request, 'ALM/inserisci_codice.html')

def cambia_password(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        password = request.POST['password']
        conferma = request.POST['conferma']
        # Check username and password combination if correct
        # user = authenticate(username=username, password=password)

        if password == conferma:
            username = request.session['user']
            conn = connect()
            aggiorna_password(conn, username, password)

            return render(request, 'ALM/login.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'ALM/cambia_password.html',
                          {'error_message': 'Le password non coincidono'})
    else:
        # No post data available, let's just show the page to the user.
        return render(request, 'ALM/inserisci_codice.html')

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

                request.session['user'] = form.cleaned_data['username']
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


