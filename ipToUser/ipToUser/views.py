from django.http import HttpResponse
from datetime import date
import re
import paramiko

today = date.today().strftime("%b\s+%d").replace('0','')
DHCPServ = '172.26.73.36'
pKey = paramiko.DSSKey.from_private_key_file('/root/.ssh/id_dsa')

def index(request):
    user = request.GET.get('user')
    ip = request.GET.get('ip')
    if user != None:
        macs = userToMac(user)
        sshToDHCP()
        return HttpResponse(macs,content_type="text/plain")
    else:
        return HttpResponse(ip)


def userToMac(user: str) -> dict:
    pattern = '^.*' + today + '.*' + user + '.*cli\s+.*$'
    macs = {}
    with open('/var/log/radius/radius.log') as f:
        for line in f:
            if re.match(pattern, line): 
                mac = line.split('cli ')[-1].split(')')[0].replace('-',':')+'\n'
                if mac in macs:
                    pass
                else:
                    macs[mac]=''
    return macs

#def macToIp(macs: dict) -> dict:



def sshToDHCP():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=DHCPServ,port=22,username='admin',pkey=pKey)
    stdin, stdout, stderr = client.exec_command('ip dhcp server print')
    print(stdout.read().decode('utf-8'))
