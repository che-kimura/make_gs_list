from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings

from .forms import InForm
from .models import EstimateInfo

def index(request):
    params = {
        'title':'MAKE ESTIMATE',
        'form':InForm(),
        'results':'',
    }
    if (request.method == 'POST'):
        params['form'] = InForm(request.POST)
        params['results'] = request.POST.get("input")
    return render(request, 'make_estimate/index.html', params)


# Create your views here.
