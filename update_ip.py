import requests
import arrow
import re
import os

target = "http://ssh.angrykittens.co.uk/update_ip"
secret = "0ranges and Lem0ns"
hostname = "freja"


def is_ip(s):
    return re.match("\d+.\d+.\d+.\d+", s)


# We need this file.
if not os.path.exists(".pdns.last"):
    open(".pdns.last", "w").close()

# Find our last IP
with open(".pdns.last") as last:
    last_ip = last.read().strip()

ip = requests.get("http://www.icanhazip.com").text.strip()

if not is_ip(ip):
    # try our backup host
    ip = requests.get("http://www.ifconfig.me/ip").text.strip()

if (is_ip(ip)) and (last_ip != ip):
    requests.post(target, data={"ip": ip, "hostname": hostname, "secret":secret})

    with open(".pdns.last", "w") as new:
        msg = "[%s] Updated IP as %s.\n" % (arrow.get().now(), ip)
        new.write(ip)
else:
    msg = "[%s] IP not changed no need for update.\n" % arrow.get().now()

with open(".pdns.log", "a") as log:
    log.write(msg)
