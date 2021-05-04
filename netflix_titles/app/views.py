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

    moviesInfo = repository.getMovies()
    movies = len(moviesInfo)

    tparams = {
        'movies': [],
        'base': 'base.html'
        }

    for i in range(movies):
        aux = {'title': moviesInfo[i].get('title'), 'director': moviesInfo[i].get('directed_by'), 'release_year': moviesInfo[i].get('release_year'), 'listed_in': moviesInfo[i].get('listed_in')}
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
               'release_year': tvShowsInfo[i].get('release_year'), 'listed_in': tvShowsInfo[i].get('listed_in')}
        tparams['tvShows'].append(aux)

    return render(request, 'tvshows.html', tparams)

def search(request):
    assert isinstance(request, HttpRequest)


    if 'keyword' in request.POST:
        keyword = request.POST['keyword']
        if keyword:
            results = repository.build_search(keyword)
            print(results)
            #mexer aqui
            return render(request, 'search_results.html', {'keyword': keyword, 'base': 'base.html' , 'results': results})
        else:
            return render(request, 'search.html', {'error': True, 'base': 'base.html'} )
    else:
        return render(request, 'search.html', {'error': False, 'base': 'base.html' } )

    '''
    tparams = {
        'base': 'base.html'
    }

    return render(request, 'search.html', tparams)
    '''
