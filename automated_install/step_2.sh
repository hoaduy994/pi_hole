IFS="/"
set -- $(pwd)
who=$3
apt update -y
apt upgrade -y
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y
apt autoremove -y
wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
tar -xf Python-3.9.1.tgz
cd Python-3.9.1
./configure --enable-optimizations
make -j 12
make altinstall
apt install python3-pip -y
apt update
cd ..
rm -rf Python-3.9.1.tgz
rm -rf Python-3.9.1
cd /root/pi_hole/monitor-dns

python3.9 -m venv venv

/root/pi_hole/monitor-dns/venv/bin/pip install -r /root/pi_hole/monitor-dns/requirements.txt
/root/pi_hole/monitor-dns/venv/bin/python3.9 /root/pi_hole/monitor-dns/send_dns_node_to_server.py
