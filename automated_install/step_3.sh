IFS="/"
set -- $(pwd)
who=$3
cd /home/dnsnode/pi_hole/monitor-dns
#send_log_to_server.service ###########################################
printf "[Unit]
Description=Send Log DNS To Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/dnsnode/pi_hole/monitor-dns
Environment=PYTHONPATH=/home/dnsnode/pi_hole/monitor-dns
ExecStart=/home/dnsnode/pi_hole/monitor-dns/venv/bin/python3.9 /home/dnsnode/pi_hole/monitor-dns/send_log_to_server.py
StandardInput=tty-force
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target\n" > /home/dnsnode/pi_hole/monitor-dns/service/send_log_to_server.service
sudo cp /home/dnsnode/pi_hole/monitor-dns/service/send_log_to_server.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable send_log_to_server.service
sudo systemctl start send_log_to_server.service

/bin/sleep 2
#monitor_dns_to_server.service ###########################################
printf "[Unit]
Description=Monitor Dns To Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/dnsnode/pi_hole/monitor-dns
Environment=PYTHONPATH=/home/dnsnode/pi_hole/monitor-dns
ExecStart=/home/dnsnode/pi_hole/monitor-dns/venv/bin/python3.9 /home/dnsnode/pi_hole/monitor-dns/send_monitor_to_server.py
StandardInput=tty-force
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target\n" > /home/dnsnode/pi_hole/monitor-dns/service/monitor_dns_to_server.service
sudo cp /home/dnsnode/pi_hole/monitor-dns/service/monitor_dns_to_server.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable monitor_dns_to_server.service
sudo systemctl start monitor_dns_to_server.service

/bin/sleep 2
#send_get_raw_data.service ###########################################

printf "[Unit]
Description=Send List Black White To Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/dnsnode/pi_hole/monitor-dns
Environment=PYTHONPATH=/home/dnsnode/pi_hole/monitor-dns
ExecStart=/home/dnsnode/pi_hole/monitor-dns/venv/bin/python3.9 /home/dnsnode/pi_hole/monitor-dns/send_get_raw_data.py
StandardInput=tty-force
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target\n" > /home/dnsnode/pi_hole/monitor-dns/service/send_get_raw_data.service
sudo cp /home/dnsnode/pi_hole/monitor-dns/service/send_get_raw_data.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable send_get_raw_data.service
sudo systemctl start send_get_raw_data.service
