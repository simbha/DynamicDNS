from flask import Flask, request, abort
from flask.ext import shelve
from flask.ext.shelve import get_shelve

app = Flask(__name__)
app.config['SHELVE_FILENAME'] = 'pydns.hosts.db'
shelve.init_app(app)

@app.route("/update_ip", methods=["POST"])
def update():
    secret = request.form.get("secret")
    ip = request.form.get("ip")
    host = request.form.get("hostname")
    # My trivially simple security. Nearly laughable really.
    if secret != "0ranges and Lem0ns":
        return abort(403)
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

app.run(host="0.0.0.0", port=4000, debug=True)