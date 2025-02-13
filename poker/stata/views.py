from django.http import HttpResponse
from django.shortcuts import render
from .models import Top, Person, Game


def get_index(request):
    persons = Person.objects.all().order_by('-score').values()
    tops = Top.objects.all()
    for i in tops:
        print(i.game.date)
    return render(request, "index.html", context={'persons':persons, 'tops':tops}) #, context={'exel':data}