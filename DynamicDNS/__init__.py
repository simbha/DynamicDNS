from flask import Flask, request, abort
from flask.ext import shelve
from flask.ext.shelve import get_shelve

app = Flask(__name__)
app.config['SHELVE_FILENAME'] = 'pydns.hosts.db'
shelve.init_app(app)

@app.route("/update_ip", methods=["POST"])
def update():
    ip = request.form.get("ip")
    host = request.form.get("hostname")
    db = get_shelve('c')
    db[str(host)] = str(ip)
    return "OK"

@app.route("/host/<name>")
def hosts(name):
    # flask gives you unicode damn it!
    return str(get_shelve("c").get(str(name), "Host not registered!"))


@app.route("/hosts")
def all_hosts():
    return "<br/>".join("%s - %s" % (x, y) for x, y in get_shelve("c").iteritems())

