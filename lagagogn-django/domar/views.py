from domar.models import Domur, Domstoll
from django.shortcuts import get_object_or_404, render


def index(request):
    latest_domar_list = Domur.objects.order_by('-date')[:20]
    domstolar = Domstoll.objects.all()
    context = {'domar': latest_domar_list, 'domstolar': domstolar}
    return render(request, 'home.html', context)


def domur(request, domstoll, slug):
    obj = get_object_or_404(Domur, slug=slug)
    context = {'domur': obj}
    return render(request, 'domur.html', context)


def domstoll(request, slug):
    obj = get_object_or_404(Domstoll, slug=slug)
    latest_domar_list = Domur.objects.filter(domstoll__slug=slug).order_by('-date')[:20]
    context = {'domstoll': obj, 'domar': latest_domar_list}
    return render(request, 'domstoll.html', context)

