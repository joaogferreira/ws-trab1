from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import requests
import random
import string

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

    moviesInfo = repository.getMovies()
    movies = len(moviesInfo)

    tparams = {
        'movies': [],
        'base': 'base.html'
        }

    for i in range(movies):
        aux = {'title': moviesInfo[i].get('title'), 'director': moviesInfo[i].get('directed_by'),
               'release_year': moviesInfo[i].get('release_year'), 'listed_in': moviesInfo[i].get('listed_in'),
               'cast': moviesInfo[i].get('cast'), 'duration': moviesInfo[i].get('duration')}

        tparams['movies'].append(aux)

    return render(request, 'movies.html', tparams)


def tvshows(request):
    assert isinstance(request, HttpRequest)

    tvShowsInfo = repository.getTvShows()
    tvShows = len(tvShowsInfo)
    tparams = {
        'tvShows': [],
        'base': 'base.html'
    }

    for i in range(tvShows):
        aux = {'title': tvShowsInfo[i].get('title'), 'director': tvShowsInfo[i].get('directed_by'),
               'release_year': tvShowsInfo[i].get('release_year'), 'listed_in': tvShowsInfo[i].get('listed_in'),
               'cast': tvShowsInfo[i].get('cast'), 'duration': tvShowsInfo[i].get('duration')}
        tparams['tvShows'].append(aux)

    return render(request, 'tvshows.html', tparams)

def search(request):
    assert isinstance(request, HttpRequest)


    if 'keyword' in request.POST:
        keyword = request.POST['keyword']
        if keyword:
            results = repository.build_search(keyword)

            return render(request, 'search_results.html', {'keyword': keyword, 'base': 'base.html' , 'results': results, 'nResults': len(results)})
        else:
            return render(request, 'search.html', {'error': True, 'base': 'base.html'} )
    else:
        return render(request, 'search.html', {'error': False, 'base': 'base.html' } )


def add(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':

        type = request.POST['type']
        title = request.POST['title']
        directed = request.POST['directed_by']
        cast = request.POST['cast']
        country = request.POST['country']
        date = request.POST['date']
        release = request.POST['release']
        duration = request.POST['duration']
        listed_in = request.POST['listed_in']

        letters = string.ascii_lowercase
        id = (''.join(random.choice(letters) for i in range(10)))

        results = repository.addTitle(id, type, title, directed, cast, country, date, release, duration, listed_in)

    return render(request, 'add.html', {'base': 'base.html'})

def search_by_release_year(request):
    assert isinstance(request, HttpRequest)

    if 'from' in request.POST and 'to' in request.POST:
        from_year = request.POST['from']
        to = request.POST['to']


        if from_year and to and from_year.isnumeric() and to.isnumeric():
            results = repository.search_year(from_year,to)

            return render(request, 'year_results.html', {'from': from_year, 'to': to, 'base': 'base.html', 'results': results, 'nResults': len(results)})
        else:
            return render(request, 'year.html', {'error': True, 'base': 'base.html'} )
    else:
        return render(request, 'year.html', {'error': False, 'base': 'base.html' } )


    return render(request, 'year.html', {'base' : 'base.html'} )


