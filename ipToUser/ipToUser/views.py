from django.http import HttpResponse
from datetime import date
import re
import paramiko
import json

today = date.today().strftime("%b\s+%d").replace('0','')
DHCPServ = '172.26.73.36'
pKey = paramiko.DSSKey.from_private_key_file('/root/.ssh/id_dsa')

def index(request):
    user = request.GET.get('user')
    ip = request.GET.get('ip')
    if user != None:
        macs = getMacs(user)
        for mac in macs.keys():
            macs[mac] = sshToFind('mac-address', mac, 2)
        return HttpResponse(json.dumps(macs),content_type="text/plain")
    else:
        mac = sshToFind('address', ip, 33)
        user = getUser(mac[0])
        return HttpResponse(user)


def getMacs(user: str) -> dict:
    pattern = '^.*' + today + '.*' + user + '.*cli\s+.*$'
    macs = {}
    with open('/var/log/radius/radius.log') as f:
        for line in f:
            if re.match(pattern, line): 
                mac = line.split('cli ')[-1].split(')')[0].replace('-',':')
                if mac in macs:
                    pass
                else:
                    macs[mac]=''
    return macs

def getUser(mac: str) -> str:
    pattern = '^.*' + today + '.*' + mac.replace(':','-') + '.*'
    user = ''
    with open('/var/log/radius/radius.log') as f:
        for line in f:
            if re.match(pattern, line): 
                user =  line.split('OK: [')[1].split(']')[0]
    return user


def sshToFind(key: str, value: str, offset: int):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=DHCPServ,port=22,username='admin',pkey=pKey)
    stdin, stdout, stderr = client.exec_command('ip dhcp-server lease print where {}={}'.format(key,value))
    ans = []
    for line in stdout.readlines():
        if value in line:
            ans.append(line.split(' ')[offset])
    client.close()
    return ans
