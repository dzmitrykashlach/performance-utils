# This script is created according to the following manual
#https://www.linuxbabe.com/ubuntu/shadowsocks-libev-proxy-server-ubuntu
#!/bin/bash

get_random_port()
{
local random_port=$(( ((RANDOM<<15)|RANDOM) % 49152 + 10000 ))
echo "$random_port"
}

port_status()
{
local status="$(nc -z 127.0.0.1 $random_port < /dev/null &>/dev/null; echo $?)"
echo "$status"
}

get_and_check_random_port()
{
while : ;
do
    random_port=$(get_random_port)
    if [ $(port_status) != "0" ]; then
            break
    fi
done
}

get_backup_ports_range()
{
  # TODO
  # Select random ports for backing up;
  echo 'port_left=12000; port_right=12010'  
}



get_and_check_random_port
apt-get install shadowsocks-libev
sed -i 's/"127.0.0.1"/"0.0.0.0"/' /etc/shadowsocks-libev/config.json
sed -i 's/8388/'"$random_port"'/g' /etc/shadowsocks-libev/config.json
# TODO:
# sed shadowsocks.sh: openssl rand -base64 20 > password - update config.json with extended password;
systemctl restart shadowsocks-libev.service
systemctl enable shadowsocks-libev.service
systemctl status shadowsocks-libev.service
# reset ufw & clean rules
ufw reset
# open ufw
ufw enable
ufw allow ssh
ufw allow $random_port
ufw logging on
ufw logging medium #log is located in /var/log/ufw.log
ufw status
systemctl restart shadowsocks-libev.service
systemctl status shadowsocks-libev.service
cat /etc/shadowsocks-libev/config.json

iptables -t nat -L PREROUTING -nv --line-number
for i in {0..1}
do
   iptables -t nat -D PREROUTING 1
done
port_left=0
port_right=0
eval $(get_backup_ports_range)
iptables -t nat -A PREROUTING -p tcp --dport $port_left:$port_right -j REDIRECT --to-port $random_port
iptables -t nat -A PREROUTING -p udp --dport $port_left:$port_right -j REDIRECT --to-port $random_port
iptables -t nat -L PREROUTING -nv --line-number
exit;
