from app.graphDBConnection import GraphDB


class Repository:
    # Get the most used weapons
    mostUsedWeapons = """
        PREFIX att:<http://global-terrorism.com/pred/>
        SELECT ?weaponName (count(?weaponName) as ?count)
        WHERE{
            ?attack att:weapon ?weapon .
            ?weapon att:name ?weaponName
        } GROUP BY ?weaponName ORDER BY DESC (?count)
        """
    #Get the number of movies
    nMovies= """
           PREFIX net:<http://netflix-titles.com/pred/>
            Select (COUNT(?movie) as ?n_movies)
                where{
                    ?movies net:type ?movie .
                        Filter(?movie = 'Movie')
                }	 
    """
    nTVShows = """
    PREFIX net:<http://netflix-titles.com/pred/>
           
    Select (COUNT(?tv_show) as ?n_tvShow)
        where{
            ?tv_shows net:type ?tv_show .
                Filter(?tv_show = 'TV Show')
        }	
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

    def getTopWeapons(self):
        list = []
        results = self.graphDB.getResults(self.mostUsedWeapons)
        for e in results[:5]:
            dic = {}
            dic['weaponName'] = e['weaponName']['value']
            dic['count'] = e['count']['value']
            list.append(dic)
        return list

    def getTopCountries(self):
        list = []
        results = self.graphDB.getResults(self.deadliestCountries)
        for e in results[:5]:
            dic = {}
            dic['countryName'] = e['countryName']['value']
            dic['count'] = e['totalKills']['value']
            list.append(dic)
        return list

    def getStatisticsSuccess(self):
        dic = {}
        results = self.graphDB.getResults(self.succeededAttacks)
        for e in results:
            dic['succeeded'] = e['attacksSuccess']['value']
            # list.append(e['attacksSuccess']['value'])
        results = self.graphDB.getResults(self.unsucceededAttacks)
        for e in results:
            dic['failed'] = e['attacksFailed']['value']
            # list.append(e['attacksFailed']['value'])
        return dic

    def getAllAttacks(self):
        list = []
        results = self.graphDB.getResults(self.allAttacks)
        for e in results:
            dic = {}
            dic['id'] = e['attack']['value'].split('/')[-1]
            dic['date'] = e['date']['value']
            dic['country'] = e['countryName']['value']
            dic['region'] = e['regionName']['value']
            dic['city'] = e['city']['value']
            dic['success'] = e['success']['value']
            dic['suicide'] = e['suicide']['value']
            dic['type'] = e['typeName']['value']
            dic['target'] = e['targetName']['value']
            dic['type'] = e['typeName']['value']
            dic['nationality'] = e['targetNationalityName']['value']
            dic['weapon'] = e['weaponName']['value']
            dic['kills'] = e['kills']['value']
            list.append(dic)
        return list

    def getAllAttacksByCountry(self, country):
        list = []
        allAttacks = """
                PREFIX att:<http://global-terrorism.com/pred/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?attack ?date ?countryName ?regionName ?city ?success ?suicide ?typeName ?targetName ?targetNationalityName ?weaponName ?kills
                    WHERE{
                        ?attack att:date ?date .
                        ?attack att:country ?country .
                        ?country att:name ?countryName .
                        ?attack att:region ?region .
                        ?region att:name ?regionName .
                        ?attack att:city ?city .
                        ?attack att:success ?success .
                        ?attack att:suicide ?suicide .
                        ?attack att:type ?type .
                        ?type att:name ?typeName .
                        ?attack att:target ?target .
                        ?target att:name ?targetName .
                        ?attack att:target_nationality ?targetNationality .
                        ?targetNationality att:name ?targetNationalityName .
                        ?attack att:weapon ?weapon .
                        ?weapon att:name ?weaponName .
                        ?attack att:kills ?kills
    					FILTER regex(?countryName, \"""" + country + """\", "i")
                } LIMIT 2000
            """
        results = self.graphDB.getResults(allAttacks)
        for e in results:
            dic = {}
            dic['id'] = e['attack']['value'].split('/')[-1]
            dic['date'] = e['date']['value']
            dic['country'] = e['countryName']['value']
            dic['region'] = e['regionName']['value']
            dic['city'] = e['city']['value']
            dic['success'] = e['success']['value']
            dic['suicide'] = e['suicide']['value']
            dic['type'] = e['typeName']['value']
            dic['target'] = e['targetName']['value']
            dic['type'] = e['typeName']['value']
            dic['nationality'] = e['targetNationalityName']['value']
            dic['weapon'] = e['weaponName']['value']
            dic['kills'] = e['kills']['value']
            list.append(dic)
        return list

    def getKillsPerYear(self):
        list = []
        results = self.graphDB.getResults(self.killsYear)
        aux = []
        for i in results:
            aux.append(int(i['kills']['value']))
        for e in results:
            dic = {}
            dic['year'] = e['attackYear']['value']
            dic['kills'] = e['kills']['value']
            dic['height'] = str((int(e['kills']['value']) / max(aux)) * 100)
            dic['max'] = str(max(aux))
            list.append(dic)
        return list

    def getAttacksPerYear(self):
        list = []
        results = self.graphDB.getResults(self.attacksYear)
        aux = []
        for i in results:
            aux.append(int(i['attacks']['value']))
        for e in results:
            dic = {}
            dic['year'] = e['attackYear']['value']
            dic['attacks'] = e['attacks']['value']
            dic['height'] = str((int(e['attacks']['value']) / max(aux)) * 100)
            dic['max'] = str(max(aux))
            list.append(dic)
        return list

    def getKillsPerYearPerCountry(self, country):
        list = []
        query = """
            PREFIX att:<http://global-terrorism.com/pred/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?attackYear (SUM (?kills) AS ?kills) ?country
            WHERE{
                ?attack att:date ?date .
                ?attack att:kills ?kills .
                ?attack att:country ?country
                FILTER(?country = <""" + country + """>)
            } GROUP BY (year(xsd:dateTime(?date)) as ?attackYear) ?country

        """
        results = self.graphDB.getResults(query)
        aux = []
        for i in results:
            aux.append(int(i['kills']['value']))
        for e in results:
            dic = {}
            dic['year'] = e['attackYear']['value']
            dic['kills'] = e['kills']['value']
            if int(e['kills']['value']) != 0:
                dic['height'] = str((int(e['kills']['value']) / max(aux)) * 100)
            else:
                dic['height'] = 0
            dic['max'] = str(max(aux))
            list.append(dic)
        return list

    def getAttacksPerYearPerCountry(self, country):
        list = []
        query = """
            PREFIX att:<http://global-terrorism.com/pred/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?attackYear (COUNT (?attack) AS ?attacks)
            WHERE{
                ?attack att:date ?date .
                ?attack att:country ?country
                FILTER(?country = <""" + country + """>)
            } GROUP BY (year(xsd:dateTime(?date)) as ?attackYear)
        """
        results = self.graphDB.getResults(query)
        aux = []
        for i in results:
            aux.append(int(i['attacks']['value']))
        for e in results:
            dic = {}
            dic['year'] = e['attackYear']['value']
            dic['attacks'] = e['attacks']['value']
            if int(e['attacks']['value']) != 0:
                dic['height'] = str((int(e['attacks']['value']) / max(aux)) * 100)
            else:
                dic['height'] = 0
            dic['max'] = str(max(aux))
            list.append(dic)
        return list

    def getAttacksNumbers(self):
        list = []
        results = self.graphDB.getResults(self.attacksNumbers)
        for e in results:
            dic = {}
            dic['country'] = e['countryName']['value']
            dic['attacks'] = e['attacks']['value']
            dic['kills'] = e['countryKills']['value']
            dic['success'] = e['attacksSuccess']['value']
            dic['fails'] = str(int(e['attacks']['value']) - int(e['attacksSuccess']['value']))
            list.append(dic)
        return list

    def getAllCountries(self):
        list = []
        results = self.graphDB.getResults(self.countriesNames)
        for e in results:
            list.append((e['country']['value'], e['countryName']['value']))
        return list

    def getAllRegions(self):
        list = []
        results = self.graphDB.getResults(self.regionsNames)
        for e in results:
            list.append((e['region']['value'], e['regionName']['value']))
        return list

    def getAllAttackTypes(self):
        list = []
        results = self.graphDB.getResults(self.attackTypes)
        for e in results:
            list.append((e['attackType']['value'], e['attackTypeName']['value']))
        return list

    def getAllWeapons(self):
        list = []
        results = self.graphDB.getResults(self.weapons)
        for e in results:
            list.append((e['weapon']['value'], e['weaponName']['value']))
        return list

    def getAllTargets(self):
        list = []
        results = self.graphDB.getResults(self.targets)
        for e in results:
            list.append((e['target']['value'], e['targetName']['value']))
        return list

    def getAllTargetNationalities(self):
        list = []
        results = self.graphDB.getResults(self.targetNationalities)
        for e in results:
            list.append((e['targetNationality']['value'], e['targetNationalityName']['value']))
        return list

    def addAttack(self, id, date, country, region, city, attack_type, weapon, target, nationality, success, suicide,
                  kills):
        query = """
        PREFIX att:<http://global-terrorism.com/pred/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        INSERT DATA {
                    att:""" + str(id) + """ att:date \"""" + str(date) + """\"^^xsd:date;
                     att:country <""" + country + """> ;
                     att:region <""" + region + """> ;
                     att:city \"""" + city + """\"^^xsd:string ;
                     att:type <""" + attack_type + """> ;
                     att:weapon <""" + weapon + """> ;
                     att:target <""" + target + """> ;
                     att:target_nationality <""" + nationality + """> ;
                     att:success """ + str(success) + """ ;
                     att:suicide """ + str(suicide) + """ ;
                     att:kills """ + str(kills) + """ .
}
        """
        return self.graphDB.add(query)

    def removeAttack(self, attack_id):
        query = """
            PREFIX att:<http://global-terrorism.com/attack/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            DELETE {?s ?p ?o}
            WHERE
            {
                ?s ?p ?o
                FILTER(?s = <http://global-terrorism.com/attack/""" + str(attack_id) + """>)
            }
        """
        return self.graphDB.add(query)

    # Generate Inferences
    def generateInferences(self):
        self.graphDB.add(self.safeGlobal)
        self.graphDB.add(self.lowGlobal)
        self.graphDB.add(self.mediumGlobal)
        self.graphDB.add(self.highGlobal)
        self.graphDB.add(self.criticalGlobal)
        self.graphDB.add(self.suicideZones)
        self.graphDB.add(self.weaponKills)

    def getRiskByCountry(self):
        list = []
        results = self.graphDB.getResults(self.riskByCountry)
        for e in results:
            dic = {}
            dic['country'] = e['countryName']['value']
            dic['risk'] = e['risk']['value']
            dic['attacks'] = e['attacks']['value']
            list.append(dic)
        return list

    def getSuicideZones(self):
        list = []
        results = self.graphDB.getResults(self.selectSuicideZones)
        for e in results:
            dic = {}
            dic['region'] = e['regionName']['value']
            dic['suicides'] = int(e['suicideAttacks']['value'])
            list.append(dic)
        return list

    def getWeaponsKills(self):
        list = []
        results = self.graphDB.getResults(self.selectWeaponKills)
        for e in results:
            dic = {}
            dic['weapon'] = e['weaponName']['value']
            dic['kills'] = e['weaponKills']['value']
            list.append(dic)
        return list
