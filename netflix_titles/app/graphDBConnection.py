from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


class GraphDB:
    connection = False;

    def __init__(self, endpoint, repo_name):
        self.endpoint = endpoint
        self.repo_name = repo_name
        self.startConnection()

    # Start graphDB connection
    def startConnection(self):
        if not self.connection:
            self.client = ApiClient(endpoint=self.endpoint)
            self.accessor = GraphDBApi(self.client)
            self.connection = True

    # Get query results
    def getResults(self, query):
        payload_query = {"query": query}
        res = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        res = json.loads(res)
        return res['results']['bindings']

    # Add query / update
    def add(self, update):
        payload_query = {"update": update}
        res = self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)
        return True



