from django.http import HttpResponse
from datetime import date
import re
import paramiko

today = date.today().strftime("%b\s+%d").replace('0','')

def index(request):
    user = request.GET.get('user')
    ip = request.GET.get('ip')
    if user != None:
        mac = userToMac(user)
        return HttpResponse(mac)
    else:
        return HttpResponse(ip)


def userToMac(user: str) -> Set{str}:
    pattern = '^.*' + today + '.*' + user + '.*$'
    mac = set()
    with open('/var/log/radius/radius.log') as f:
        for line in f:
            if re.match(pattern, line):   
                mac.add(line.split(' ')[-1].split(')')[0].replace('-',':'))    
    return mac
