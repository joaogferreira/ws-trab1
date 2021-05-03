from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import requests

from app.repository import Repository

repo_name = "netflix"
endpoint = "http://localhost:7200"
repository = Repository(repo_name, endpoint)


# Create your views here.
def home(request):
    assert isinstance(request, HttpRequest)

    movies = repository.getNumberMovies()
    tvShows = repository.getNumberTvShows()

    tparams= {
            'base': 'base.html',
            'movies': movies[0]['n_movies'],
            'tv_shows': tvShows[0]['n_tvShow']
        }

    return render(request, 'home.html', tparams)

