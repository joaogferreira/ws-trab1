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

def movies(request):
    assert isinstance(request, HttpRequest)

    tparams = {
        'movies' : [
            {'title': 'O Padrinho', 'director': 'Director X', 'release_year': 'Year Y', 'listed_in': 'comedy'},
            {'title': 'O Padrinho II', 'director': 'Director A', 'release_year': 'Year Z', 'listed_in': 'drama'},
            {'title': 'O Padrinho III', 'director': 'Director B', 'release_year': 'Year W', 'listed_in': 'comedy and drama'},
            {'title': 'O Grande Chefão', 'director': 'Director C', 'release_year': 'Year H', 'listed_in': 'war'},
        ],
        'base' : 'base.html'
    }

    return render(request, 'movies.html', tparams)


def tvshows(request):
    assert isinstance(request, HttpRequest)

    tparams = {
        'movies': [
            {'title': 'Serie I', 'director': 'Director Quim Barreiros', 'release_year': '2021', 'listed_in': 'comedy'},
            {'title': 'Serie II', 'director': 'Director Yashin', 'release_year': '2011', 'listed_in': 'drama'},
            {'title': 'Serie III', 'director': 'Director Iker Casillas', 'release_year': '2010', 'listed_in': 'comedy and drama'},
            {'title': 'Serie IV', 'director': 'Director C', 'release_year': 'Year H', 'listed_in': 'war'},
        ],
        'base': 'base.html'
    }

    return render(request, 'tvshows.html', tparams)

def search(request):
    assert isinstance(request, HttpRequest)

    tparams = {
        'base': 'base.html'
    }

    return render(request, 'search.html', tparams)

