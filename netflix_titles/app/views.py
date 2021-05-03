from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import requests

from app.repository import Repository

#repo_name = ""
#endpoint = "http://localhost:7200"
#repository = Repository(repo_name, endpoint)


# Create your views here.
def home(request):
    assert isinstance(request, HttpRequest)

    tparams= {'base': 'base.html'}

    return render(request, 'home.html', tparams)

