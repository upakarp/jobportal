from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render


def index(request):
    return render(request, 'base.html')

