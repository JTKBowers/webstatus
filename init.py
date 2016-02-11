import os
import psycopg2

try:
    conn = psycopg2.connect("dbname=webstatus user=postgres")
except psycopg2.OperationalError:
    if (input("Create database 'webstatus' (Y/n)? ") != 'n'):
        print("Creating database...")
        r = os.system("createdb -U postgres webstatus")
        if r != 0:
            print ("Error creating database")
            exit()
        conn = psycopg2.connect("dbname=webstatus user=postgres")
    else:
        exit()

cur = conn.cursor()

print ("Creating table...")
cur.execute("CREATE TABLE status (status boolean, ts timestamp);")

print ("Committing to db...")
conn.commit()
cur.close()
conn.close()
print ("Done!")
