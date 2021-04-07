from django.http import HttpResponse
import re


def index(request):
    user = request.GET.get('user')
    ip = request.GET.get('ip')
    if user != None:
        mac = userToip(user)
        return HttpResponse(mac)
    else:
        return HttpResponse(ip)

def userToip(user):
    pattern = user
    with open('/var/log/radius/radius.log') as f:
        for line in f:
            if re.search(pattern, line):
                lastMatch = line   
    return lastMatch.split(' ')[-1].split(')')[0].replace('-',':')    

