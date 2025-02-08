from django.http import HttpResponse
from django.shortcuts import render
from .models import Top, Person, Game


def get_index(request):
    data = Person.objects.all().order_by('-score').values()
    for d in data:
        print(d)
    return render(request, "index.html", context={'data':data}) #, context={'exel':data}