from django.shortcuts import render
from django.http import HttpResponse
from domar.models import Domur
from django.shortcuts import get_object_or_404, render
from django.template import loader


def index(request):
    latest_domar_list = Domur.objects.order_by('-date')[:20]
    context = {'domar': latest_domar_list}
    return render(request, 'home.html', context)


def domur(request, domstoll, identifier):
    identifier = identifier.replace('-', '/')
    obj = get_object_or_404(Domur, identifier=identifier)
    context = {'domur': obj}
    return render(request, 'domur.html', context)

