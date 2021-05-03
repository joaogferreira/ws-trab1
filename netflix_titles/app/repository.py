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

    # Get countries with more kills
    deadliestCountries = """
        PREFIX att:<http://global-terrorism.com/pred/>
        SELECT ?countryName (sum(?nKills) as ?totalKills)
        WHERE{
            ?attack att:kills ?nKills .
            ?attack att:country ?country .
            ?country att:name ?countryName
        } GROUP BY ?countryName ORDER BY DESC (?totalKills)
        """

    # All attacks with all informations
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
                FILTER (?kills>10)
        } LIMIT 2000
    """

    # Number of kills per year
    killsYear = """
        PREFIX att:<http://global-terrorism.com/pred/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?attackYear (SUM (?kills) AS ?kills)
        WHERE{
            ?attack att:date ?date .
            ?attack att:kills ?kills .
        } GROUP BY (year(xsd:dateTime(?date)) as ?attackYear)

    """

    # Number of attacks per year
    attacksYear = """
            PREFIX att:<http://global-terrorism.com/pred/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?attackYear (COUNT (?attack) AS ?attacks)
            WHERE{
                ?attack att:date ?date .
            } GROUP BY (year(xsd:dateTime(?date)) as ?attackYear)

        """

    # Number of succeeded attacks
    succeededAttacks = """

        PREFIX att:<http://global-terrorism.com/pred/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT (COUNT(?success) AS ?attacksSuccess)
        WHERE{
                ?attack att:success ?success .
                FILTER (?success = 1) .
            }

    """

    # Number of failed attacks
    unsucceededAttacks = """
        PREFIX att:<http://global-terrorism.com/pred/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT (COUNT(?success) AS ?attacksFailed)
        WHERE{
                ?attack att:success ?success .
                FILTER (?success = 0) .
            }
    """

    # Number of attacks, kills and succeeded attacks by country
    attacksNumbers = """
        PREFIX att:<http://global-terrorism.com/pred/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT ?countryName (COUNT(?attack) AS ?attacks) (SUM (?kills) AS ?countryKills) (SUM(?success) AS ?attacksSuccess)
        WHERE
            {
                ?attack att:country ?country .
                ?country att:name ?countryName .
                ?attack att:kills ?kills .
                ?attack att:success ?success .
            }

        GROUP BY ?countryName
        ORDER BY DESC (?attacks)
    """

    # Countries names list
    countriesNames = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?country ?countryName
    WHERE
        {
            ?attack att:country ?country .
            ?country att:name ?countryName
        } ORDER BY (?countryName)
    """

    # Regions names list
    regionsNames = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?region ?regionName
    WHERE
        {
            ?attack att:region ?region .
            ?region att:name ?regionName
        } ORDER BY (?regionName)
    """

    # Attacks types list
    attackTypes = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?attackType ?attackTypeName
    WHERE
        {
            ?attack att:type ?attackType .
            ?attackType att:name ?attackTypeName
        } ORDER BY (?attackTypeName)
    """

    # Weapons names list
    weapons = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?weapon ?weaponName
    WHERE
        {
            ?attack att:weapon ?weapon .
            ?weapon att:name ?weaponName
        } ORDER BY (?weaponName)
    """

    # Targets list
    targets = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?target ?targetName
    WHERE
        {
            ?attack att:target ?target .
            ?target att:name ?targetName
        } ORDER BY (?targetName)
    """

    # Targets nationality list
    targetNationalities = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?targetNationality ?targetNationalityName
    WHERE
        {
            ?attack att:target_nationality ?targetNationality .
            ?targetNationality att:name ?targetNationalityName
        } ORDER BY (?targetNationalityName)
    """

    # Generate Inference: Global critical zones according attacks numbers

    safeGlobal = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT {?country att:risk "Safe"}
        WHERE {
            {
                SELECT (COUNT(?attack) AS ?attacks) ?country
                WHERE {
                    ?attack att:country ?country
                } GROUP BY ?country HAVING (?attacks <= 10)
            }
        }
    """

    lowGlobal = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT {?country att:risk "Low"}
        WHERE {
            {
                SELECT (COUNT(?attack) AS ?attacks) ?country
                WHERE {
                    ?attack att:country ?country
                } GROUP BY ?country HAVING (?attacks > 10 && ?attacks <= 100)
            }
        }
    """

    mediumGlobal = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT {?country att:risk "Medium"}
        WHERE {
            {
                SELECT (COUNT(?attack) AS ?attacks) ?country
                WHERE {
                    ?attack att:country ?country
                } GROUP BY ?country HAVING (?attacks > 100 && ?attacks <= 1000 )
            }
        }
    """

    highGlobal = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT {?country att:risk "High"}
        WHERE {
            {
                SELECT (COUNT(?attack) AS ?attacks) ?country
                WHERE {
                    ?attack att:country ?country
                } GROUP BY ?country HAVING (?attacks > 1000 && ?attacks <= 3000 )
            }
        }
    """

    criticalGlobal = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT {?country att:risk "Critical"}
        WHERE {
            {
                SELECT (COUNT(?attack) AS ?attacks) ?country
                WHERE {
                    ?attack att:country ?country
                } GROUP BY ?country HAVING (?attacks > 3000 )
            }
        }
    """

    # Generate Inference: Global critical suicide zones according suicide attacks numbers
    suicideZones = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT {?region att:suicideAttacks ?suicideAttacks}
    WHERE {
        {
            SELECT (SUM(?suicide) AS ?suicideAttacks) ?region
            WHERE {
                ?attack att:region ?region .
                ?attack att:suicide ?suicide
            } GROUP BY ?region
        }
    }
    """

    # Generate Inference: Critical weapons according kills
    weaponKills = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT {?weapon att:kills ?weaponKills}
    WHERE {
        {
            SELECT (SUM(?kills) AS ?weaponKills) ?weapon
            WHERE {
                ?attack att:weapon ?weapon .
                ?attack att:kills ?kills
            } GROUP BY ?weapon
        }
    }
    """

    # Get risk of each country
    riskByCountry = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?countryName ?risk (COUNT(?attack) AS ?attacks)
        WHERE {
            ?attack att:country ?country .
            ?country att:name ?countryName .
            ?country att:risk ?risk .
        } GROUP BY ?countryName ?risk ORDER BY DESC (?attacks)
    """

    # Get suicide regions
    selectSuicideZones = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?regionName ?suicideAttacks
    WHERE {
        ?region att:name ?regionName .
        ?region att:suicideAttacks ?suicideAttacks
    } ORDER BY DESC (?suicideAttacks)
    """

    # Get weapon kills numbers
    selectWeaponKills = """
    PREFIX att:<http://global-terrorism.com/pred/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?weaponName ?weaponKills
    WHERE {
        ?attack att:weapon ?weapon .
        ?weapon att:name ?weaponName .
        ?weapon att:kills ?weaponKills
    } ORDER BY DESC(?weaponKills)
    """

    def __init__(self, repo_name, endpoint):
        self.graphDB = GraphDB(endpoint, repo_name)

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
