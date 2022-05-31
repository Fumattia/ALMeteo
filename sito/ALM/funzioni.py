import smtplib
import string
import random
from .mysql_database import *

length_of_string = 8
global codice

def sendcodice(username):
    codice = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    print(codice)
    oggetto = "Codice di verifica password!\n\n"
    contenuto = "Benvenuto" + username + "Inserisci il sequente codice nel riquadro:" + codice
    messaggio = oggetto + contenuto

    conn = connect()
    destinatario = seleziona_dato(conn, "Utenti", "Email", "Username", username)
    email = smtplib.SMTP("smtp.gmail.com", 587)
    email.ehlo()
    email.starttls()
    email.login("almeteo.gestione@gmail.com", "ALMaccount11")
    email.sendmail("almeteo.gestione@gmail.com", destinatario[0][0], messaggio)
    email.quit()

    return codice, destinatario[0][0]


def controlla(cod):
    if cod == codice:
        return True
    else:
        return False