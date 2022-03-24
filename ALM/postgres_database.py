import psycopg2

def connect():
    conn = None
    try:
        conn = psycopg2.connect(
            host="ec2-99-80-170-190.eu-west-1.compute.amazonaws.com",
            database="dh8vdbsc8dest",
            user="pnbyqwdjwinlmn",
            password="78070ca130941b336a0a3bafe2cdca4b29137c1b453ba3352f9a74f98b14c560")

        print("connesso")

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def nuovo_utente(conn, username, nome, cognome, email, numero):
    cur = conn.cursor()
    query = """INSERT INTO "public"."utenti" ("id_utente", "Nome", "Cognome", "Email", "Numero_cellulare") VALUES (%s, %s, %s, %s,%s)"""
    elementi = (username, nome, cognome, email, numero)
    cur.execute(query, elementi)
    conn.commit()

def close(conn):
    cursor = conn.cursor()
    cursor.close()
    print("connessione chiusa")


