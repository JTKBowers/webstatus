import jinja2
import psycopg2
from flask import Flask


app = Flask(__name__)

template = jinja2.Template(open('status.html').read())

conn = psycopg2.connect("dbname=webstatus user=postgres")
cur = conn.cursor()


@app.route("/")
def status():
    web_status = {}

    cur.execute("SELECT status FROM status LIMIT 1;")
    web_status['internet'] = cur.fetchone()[0]

    cur.execute("SELECT count(status) FROM status WHERE ts > NOW() - INTERVAL '1 hour';")
    hour_count = cur.fetchone()[0]
    #assume hour count is just 120 (ignore timing jitter)
    #hour_count = 120

    cur.execute("SELECT count(status) FROM status WHERE status = true AND ts > NOW() - INTERVAL '1 hour';")
    web_status['hour_uptime'] = 100*cur.fetchone()[0] / hour_count

    #assume hour count is just 120*24 (ignore timing jitter)
    #day_count = 2880
    cur.execute("SELECT count(status) FROM status WHERE ts > NOW() - INTERVAL '1 day';")
    day_count = cur.fetchone()[0]
    cur.execute("SELECT count(status) FROM status WHERE status = true AND ts > NOW() - INTERVAL '1 day';")
    web_status['day_uptime'] = 100*cur.fetchone()[0]/day_count

    #assume hour count is just 120*24*7 (ignore timing jitter)
    #week_count = 20160
    cur.execute("SELECT count(status) FROM status WHERE ts > NOW() - INTERVAL '1 week';")
    week_count = cur.fetchone()[0]
    cur.execute("SELECT count(status) FROM status WHERE status = true AND ts > NOW() - INTERVAL '1 week';")
    web_status['week_uptime'] = 100* cur.fetchone()[0]/week_count

    return template.render(web_status)

if __name__ == "__main__":
    app.run()
