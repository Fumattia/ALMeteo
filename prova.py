# Importazione del modulo MySQL
import mysql.connector
# Connessione a MySQL
connessione = mysql.connector.connect(
# Parametri per la connessione
  host="fumacasa.duckdns.org",
  user="user",
  password="password",
  db="ALMeteo"
)
# Stampa dell'handle di connessione
print(connessione)