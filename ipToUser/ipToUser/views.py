from django.http import HttpResponse

def index(request):
    print("hello")
    return HttpResponse('Hello')