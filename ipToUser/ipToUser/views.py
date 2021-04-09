from django.http import HttpResponse
from datetime import date
import re
import paramiko

today = date.today().strftime("%b\s+%d").replace('0','')

def index(request):
    user = request.GET.get('user')
    ip = request.GET.get('ip')
    if user != None:
        macs = userToMac(user)
        return HttpResponse(macs.keys(),content_type="text/plain")
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
