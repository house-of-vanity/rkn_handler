# Bird setup for passing RKN blacklists.

It uses `bird` on Linux as BGP anouncer. My hardware is `RouterBOARD 750G r2`, but you can use any you want/have.

###How to use:

1. Install `bird`
2. Install `python3` if you don't have it yet.
3. Minimal `bird` config is presented here. Read comments inside.
4. Run `bgp_getter.py` to get last RKN blacklisted IP, generate `bird` config and restart bird service. Run it using cron for instance.

Also RouterOS minimal config looks like this:
* 10.0.100.100 - is my VPN gateway.
* 192.168.88.149 - is my Linux box running bird.
* 192.168.88.1 - is my router
```shell
/routing bgp peer
add address-families=ip as-override=no comment=\
    "https://github.com/house-of-vanity/rkn_handler" default-originate=never \
    disabled=no hold-time=4m in-filter=bgp_in instance=local \
    multihop=yes name=miku \
    nexthop-choice=default out-filter="" passive=no remote-address=\
    192.168.88.149 remote-as=65433 remove-private-as=no route-reflect=no \
    tcp-md5-key="" ttl=default use-bfd=no

/routing filter
add action=accept \
    chain=bgp_in comment="Set nexthop to VPN" \
    disabled=no invert-match=no \
    set-bgp-prepend-path="" \
    set-in-nexthop=10.0.100.100 \

/routing bgp instance
add as=64999 client-to-client-reflection=yes \
    disabled=no ignore-as-path-len=yes name=local out-filter="" \
    redistribute-connected=no redistribute-ospf=no redistribute-other-bgp=no \
    redistribute-rip=no redistribute-static=no router-id=192.168.88.1 \
    routing-table=""
```

P.S.
Change ACCURACY parameter if you router can handle more/less prefixes.
