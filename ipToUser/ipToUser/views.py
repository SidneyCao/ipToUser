from django.http import HttpResponse
from datetime import date
import re
import paramiko

today = date.today().strftime("%b  %d")

def index(request):
    user = request.GET.get('user')
    ip = request.GET.get('ip')
    if user != None:
        mac = userToMac(user)
        return HttpResponse(mac)
    else:
        return HttpResponse(ip)


def userToMac(user):
    pattern = '.*' + user + '.*' + today + '.*'
    with open('/var/log/radius/radius.log') as f:
        for line in f:
            if re.search(pattern, line):
                #lastMatch = line   
                print(line)
    #return lastMatch.split(' ')[-1].split(')')[0].replace('-',':')    
    return
#def macToip(mac):
