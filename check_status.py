import os, time
import psycopg2

def is_up(host='8.8.8.8'):
    return os.system("ping -c 1 -w2 " + host + " > /dev/null 2>&1") == 0

# Call is_up every period seconds, and insert the results into the postgres db
def monitor(period=30):
    conn = psycopg2.connect("dbname=webstatus user=postgres")
    cur = conn.cursor()
    while(True):
        cur.execute("INSERT INTO status VALUES (%s, now())", (is_up(),))
        conn.commit()
        time.sleep(period)
    cur.close()
    conn.close()

if __name__ == '__main__':
    #hostname = "8.8.8.8"
    #print (is_up(hostname))
    monitor()
