import mysql.connector
import hashlib

def connect():
    conn = None
    try:
        conn = mysql.connector.connect(
            # Parametri per la connessione
            host="fumacasa.duckdns.org",
            user="user",
            password="password",
            db="ALMeteo"
        )

        print("connesso")

        return conn

    except:
        return None

def nuovo_utente(conn, username, password, nome, cognome, email, numero):
    cur = conn.cursor()
    password = hashlib.sha1(password.encode())
    print("ciao")
    u = "Utenti"
    query = """INSERT INTO `ALMeteo`.`""" + u +  """` (`Username`, `Nome`, `Cognome`, `Email`, `Numero_cellulare`, `password`) VALUES (%s, %s, %s, %s,%s,%s)"""
    elementi = (username, nome, cognome, email, numero, password.hexdigest())
    print(query, elementi)
    cur.execute(query, elementi)
    conn.commit()

def nuova_stazione(conn, posizione, username, codice_stazione):
    cur = conn.cursor()
    query = """INSERT INTO `ALMeteo`.`Stazioni` (`Posizione`, `Id_utente`, `Codice_stazione`) VALUES (%s,%s,%s)"""
    elementi = (posizione, username, codice_stazione)
    print(query, elementi)
    cur.execute(query, elementi)
    conn.commit()

def seleziona_dato(conn, tabella, rigas, rigav, valore):
    cur = conn.cursor()
    query = """SELECT `""" + rigas + """` FROM `ALMeteo`.`""" + tabella + """` WHERE `""" + rigav + """`='""" + valore + """'"""
    print(query)
    cur.execute(query)
    id = cur.fetchall()
    print(id)
    close(conn)
    return id

def seleziona(conn, tabella, limit):
    cur = conn.cursor()
    query = """SELECT * FROM `ALMeteo`.`""" + tabella + """` ORDER BY `ID` DESC LIMIT """ + str(limit)
    print(query)
    cur.execute(query)
    risultato = cur.fetchall()
    #print(risultato)
    close(conn)
    return risultato

def seleziona_mirata(conn, tabella, colonna, valore, limit):
    cur = conn.cursor()
    query = """SELECT * FROM `ALMeteo`.`""" + tabella + """` WHERE `""" + colonna + """`='""" + valore + """' ORDER BY `ID` DESC LIMIT """ + str(limit)
    print(query)
    cur.execute(query)
    risultato = cur.fetchall()
    #print(risultato)
    close(conn)
    return risultato

def aggiorna_password(conn, username, password):
    cur = conn.cursor()
    query1 = """SELECT `ID_utente` FROM `ALMeteo`.`Utenti` WHERE `Username`='""" + username + """'"""
    print(query1)
    cur.execute(query1)
    id = cur.fetchall()[0][0]
    password = hashlib.sha1(password.encode())
    password = password.hexdigest()
    query = """UPDATE `ALMeteo`.`Utenti` SET `password`='""" + password + """' WHERE  `ID_utente`=""" + str(id)
    print(query)
    cur.execute(query)
    conn.commit()



def logga(request, username, password):
    try:
        conn = connect()
        cur = conn.cursor()
        query = """SELECT `password` FROM `ALMeteo`.`Utenti` where `Username` = %s"""
        cur.execute(query, (username,))
        password_hash = cur.fetchone()
        password_hash = password_hash[0]
        print(password_hash)
        print(hashlib.sha1(password.encode()).hexdigest())
        if hashlib.sha1(password.encode()).hexdigest() == password_hash:
            request.session.flush()
            close(conn)
            return username
        else:
            request.session.cycle_key()
            print("ciao")
            close(conn)
            return None
    except  Exception as e:
        print(repr(e))
        return None



def close(conn):
    cursor = conn.cursor()
    cursor.close()
    print("connessione chiusa")


