from django.http import HttpResponse
import re


def index(request):
    user = request.GET.get('user')
    ip = request.GET.get('ip')
    if user != None:
        userToip(user)
        return HttpResponse(user)
    else:
        return HttpResponse(ip)

def userToip(user):
    pattern = user
    with open('/var/log/radius/radius.log') as f:
        for line in f:
            if re.search(pattern, line):
                print(line)
            

