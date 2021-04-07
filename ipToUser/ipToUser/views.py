from django.http import HttpResponse

def index(request):
    user = request.GET.get('user')
    return HttpResponse(user)