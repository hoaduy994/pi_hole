ip=['11.11.11.11','22.22.22.22']
f = open("/etc/dnsmasq.d/01-pihole.conf", "r")
check = True
# while check:
str_=f.read()
string= str_.split("\n")
s=0
for row in string:
    print(row)
    if "server" in row:
        str_=str_.replace(row,f'server={ip[s]}')
        s+=1
print(str_)
with open("/etc/dnsmasq.d/01-pihole.conf",'w',encoding = 'utf-8') as f:
    f.write(str_)
