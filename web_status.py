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

    # Get the most recent status
    cur.execute("SELECT status FROM status LIMIT 1;")
    web_status['internet'] = cur.fetchone()[0]

    # get the time since the last status change
    if web_status['internet']:
        cur.execute("SELECT now() - ts FROM status WHERE status = false ORDER BY ts DESC LIMIT 1;")
    else:
        cur.execute("SELECT now() - ts FROM status WHERE status = true ORDER BY ts DESC LIMIT 1;")
    time = cur.fetchone()

    if time is None:
        web_status['time'] = "forever"
    else:
        web_status['time'] = time[0]

    # Get the number of updates in the last hour
    cur.execute("SELECT count(status) FROM status WHERE ts > NOW() - INTERVAL '1 hour';")
    hour_count = cur.fetchone()[0]

    cur.execute("SELECT count(status) FROM status WHERE status = true AND ts > NOW() - INTERVAL '1 hour';")
    web_status['hour_uptime'] = 100*cur.fetchone()[0] / hour_count

    # Get the number of updates in the last day
    cur.execute("SELECT count(status) FROM status WHERE ts > NOW() - INTERVAL '1 day';")
    day_count = cur.fetchone()[0]
    cur.execute("SELECT count(status) FROM status WHERE status = true AND ts > NOW() - INTERVAL '1 day';")
    web_status['day_uptime'] = 100*cur.fetchone()[0]/day_count

    # Get the number of updates in the last week
    cur.execute("SELECT count(status) FROM status WHERE ts > NOW() - INTERVAL '1 week';")
    week_count = cur.fetchone()[0]
    cur.execute("SELECT count(status) FROM status WHERE status = true AND ts > NOW() - INTERVAL '1 week';")
    web_status['week_uptime'] = 100* cur.fetchone()[0]/week_count

    return template.render(web_status)

if __name__ == "__main__":
    app.run()
