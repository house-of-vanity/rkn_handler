import ipaddress

OUT_FILE = "/etc/bird/prefixlist.txt"

with open('/root/rkn_ip_dump.csv') as f:
    ips = f.read().decode('iso-8859-1')
    ips = ips.split(' | ')
clean = list()
k = 1
for i in ips:
    if k%100000 == 0:
        print('Processed %s lines' % k)
    try:
        ipaddress.ip_address(i)
        clean.append(i)
    except ValueError:
        for z in i.split(';'):
            try:
                ipaddress.ip_address(z)
                clean.append(z)
            except:
                pass
    k += 1

print('Found clean IPs - ', len(clean), 'All entries - ', len(ips))
ipv4 = list()
k = 1
print('Getting rid of IPv6 lines.')
for ip in clean:
    if k%10000 == 0:
        print('Found %s IPv6 lines.' % k)
        k += 1

    if isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address):
        ipv4.append(ip)
    else:
        k += 1
print('Ditched %s IPv6 lines.' % k)
print('Total IPv4 lines - %s' % len(ipv4))
with open(OUT_FILE, "w") as conf_file:
  conf_file.write("\n".join(list(map('route {}/32 reject;'.format, ipv4))))
