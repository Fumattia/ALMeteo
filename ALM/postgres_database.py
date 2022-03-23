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

        return conn.cursor()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def close(cursor):
    cursor.close()
    print("connessione chiusa")

if __name__ == '__main__':
    cur = connect()
    close(cur)

