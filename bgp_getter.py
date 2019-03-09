import urllib.request
import subprocess
# change ACCURACY if your hardware can't stand 
# amount of prefixes. e.x. RouterBOARD 750G r2
# can handle /28
ACCURACY = 28
IP_URL = "https://rkn.darkbyte.ru/openvpn.php?show=all&groupby=%s" % ACCURACY
OUT_TEMPLATE = "route %s/%s reject;"
OUT_FILE = "/etc/bird/prefixlist.txt"

print("Fetching content from %s" % IP_URL)
contents = urllib.request.urlopen(IP_URL).read().decode('utf-8').split('group by /%s subnets' % ACCURACY)[1].split('\n')
ips = list()
out = ''
for line in contents:
  if len(line) > 0:
    if line[0] != "#":
      ips.append(line.split()[2])
print("Found %s banned IP merged with %s mask." % (len(ips), ACCURACY))
print("Building bird conf file %s using '%s' as template" % (OUT_FILE, OUT_TEMPLATE))
for ip in ips:
  out += (OUT_TEMPLATE % (ip, ACCURACY)) + '\n'
with open(OUT_FILE, "w") as conf_file:
  conf_file.write(out)
subprocess.run(["systemctl", "restart", "bird"])
