from app.graphDBConnection import GraphDB


class Repository:

    #Get the number of movies
    nMovies= """
           PREFIX net:<http://netflix-titles.com/pred/>
            Select (COUNT(?movie) as ?n_movies)
                where{
                    ?movies net:type ?movie .
                        Filter(?movie = 'Movie')
                }	 
    """

    # Get the number of movies
    nTVShows = """
    PREFIX net:<http://netflix-titles.com/pred/>
           
    Select (COUNT(?tv_show) as ?n_tvShow)
        where{
            ?tv_shows net:type ?tv_show .
                Filter(?tv_show = 'TV Show')
        }	
    """

    # Get movies
    movies = """
    PREFIX net:<http://netflix-titles.com/pred/>
           
    Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in
        where{
            ?film net:type "Movie" .
            ?film net:title ?title .
            ?film net:directed_by ?directed_by .
            ?film net:cast ?cast .
            ?film net:country ?country .
            ?film net:date_added ?date_added .
            ?film net:release_year ?release_year .
            ?film net:duration ?duration .
            ?film net:listed_in ?listed_in .
        }
        Limit 10
    """

    tvShows ="""
    PREFIX net:<http://netflix-titles.com/pred/>
           
    Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in
        where{
            ?film net:type "TV Show" .
            ?film net:title ?title .
            ?film net:directed_by ?directed_by .
            ?film net:cast ?cast .
            ?film net:country ?country .
            ?film net:date_added ?date_added .
            ?film net:release_year ?release_year .
            ?film net:duration ?duration .
            ?film net:listed_in ?listed_in .
        }
        Limit 10
    """


    def __init__(self, repo_name, endpoint):
        self.graphDB = GraphDB(endpoint, repo_name)

    def getNumberMovies(self):
        list = []
        res = self.graphDB.getResults(self.nMovies)
        for i in res[:5]:
            dic = {}
            dic['n_movies'] = i['n_movies']['value']
            list.append(dic)
        return list

    def getNumberTvShows(self):
        list = []
        res = self.graphDB.getResults(self.nTVShows)
        for i in res[:5]:
            dic = {}
            dic['n_tvShow'] = i['n_tvShow']['value']
            list.append(dic)
        return list

    def getMovies(self):
        list = []
        res = self.graphDB.getResults(self.movies)
        for i in res:
            dic = {}
            dic['title'] = i['title']['value']
            dic['directed_by'] = i['directed_by']['value']
            dic['cast'] = i['cast']['value']
            dic['country'] = i['country']['value']
            dic['date_added'] = i['date_added']['value']
            dic['release_year'] = i['release_year']['value']
            dic['duration'] = i['duration']['value']
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list

    def getTvShows(self):
        list = []
        res = self.graphDB.getResults(self.tvShows)
        for i in res:
            dic = {}
            dic['title'] = i['title']['value']
            dic['directed_by'] = i['directed_by']['value']
            dic['cast'] = i['cast']['value']
            dic['country'] = i['country']['value']
            dic['date_added'] = i['date_added']['value']
            dic['release_year'] = i['release_year']['value']
            dic['duration'] = i['duration']['value']
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list

