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

    directors = """
    PREFIX net:<http://netflix-titles.com/pred/>
    
    Select distinct ?director
        where{
            ?film net:directed_by ?director .
        }
    """

    titles = """
    PREFIX net:<http://netflix-titles.com/pred/>
    
    Select distinct ?title
        where{
            ?film net:title ?title .
        }
    """

    categories = """
    PREFIX net: < http: // netflix - titles.com / pred / >

    Select distinct ?listed_in
        where{ 
        ?film net: listed_in ?listed_in.
    }
    """

    actores = """
    PREFIX net:<http://netflix-titles.com/pred/>

    Select distinct ?cast
        where{
            ?film net:cast ?cast .
        }
    """

    search = """
    PREFIX net:<http://netflix-titles.com/pred/>

    Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in
        where{
            ?film net:type ?type .
            ?film net:title ?title .
            ?film net:directed_by ?directed_by .
            ?film net:cast ?cast .
            ?film net:country ?country .
            ?film net:date_added ?date_added .
            ?film net:release_year ?release_year .
            ?film net:duration ?duration .
            ?film net:listed_in ?listed_in .
        filter ( contains (?title, 'Casa') || contains (?directed_by, 'Casa') || contains (?cast, 'Casa') || contains(?listed_in, 'Casa'))
    
        }
    """

    def build_search(self, keyword):
        query_base = "PREFIX net:<http://netflix-titles.com/pred/> Select ?film ?type ?title ?directed_by ?cast ?country ?date_added ?release_year ?duration ?listed_in where{ ?film net:type ?type . ?film net:title ?title . ?film net:directed_by ?directed_by . ?film net:cast ?cast . ?film net:country ?country . ?film net:date_added ?date_added . ?film net:release_year ?release_year . ?film net:duration ?duration . ?film net:listed_in ?listed_in ."
        aux = " filter ( regex (?title, '" + keyword +"', 'i' ) || regex (?directed_by, '" + keyword +"', 'i') || regex (?cast, '" + keyword +"', 'i') || regex (?listed_in, '" + keyword +"', 'i'))}"
        query_base = query_base + aux

        list= []
        res = self.graphDB.getResults(query_base)
        for i in res:
            dic = {}
            dic['type'] = i['type']['value']
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

    def getDirectors(self):
        list = []
        res = self.graphDB.getResults(self.directors)
        for i in res:
            dic = {}
            dic['director'] = i['director']['value']
            list.append(dic)
        return list

    def getTitles(self):
        list = []
        res = self.graphDB.getResults(self.titles)
        for i in res:
            dic = {}
            dic['title'] = i['title']['value']
            list.append(dic)
        return list

    def getCategories(self):
        list = []
        res = self.graphDB.getResults(self.categories)
        for i in res:
            dic = {}
            dic['listed_in'] = i['listed_in']['value']
            list.append(dic)
        return list

    def getActors(self):
        list = []
        res = self.graphDB.getResults(self.actores)
        for i in res:
            dic = {}
            dic['cast'] = i['cast']['value']
            list.append(dic)
        return list