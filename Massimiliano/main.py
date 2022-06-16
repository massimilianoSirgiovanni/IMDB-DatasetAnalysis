import networkx as nx
import time
from yearsFunctions import *

actorToIndex = {}   # Dictionary that return the index of a given actor

indexToActor = {}   # Dictionary that return the actor name for a given index

movieToIndex = {}   # Dictionary that return the index of a given movie

indexToMovie = {}   # Dictionary that return the movie name for a given index

def createGraph(fileName):
    file = open(fileName, "r")  # Open file
    index = 0   # Index link to actors and movies
    graph = nx.Graph()  # Graph Initialization
    for line in file:   # Scan the file line by line
        textLine = line.rstrip('\n').split('\t')    # Insert the couple (actor, movie) in a variable
        index = addActor(graph, textLine[0], index)
        index = addMovie(graph, textLine[1], index)
        graph.add_edge(actorToIndex[textLine[0]], movieToIndex[textLine[1]])    # Add an edge between actor and movie
        print(extractYear(textLine[1]))
    file.close()
    return graph


def addActor(graph, actor, idActor):
    # Verify if actor is not in dictionaries, if so the method add it in the dictionary and in the graph
    if actor not in actorToIndex:
        actorToIndex[actor] = idActor
        indexToActor[idActor] = actor
        graph.add_node(idActor, bipartite=0)     # Create node for the actor
        idActor = idActor + 1
    return idActor   # If the actor is already in the dictionary the id won't change

def addMovie(graph, movie, idMovie):
    # Verify if movie is not in dictionaries, if so the method add it in the dictionary and in the graph
    if movie not in movieToIndex:
        movieToIndex[movie] = idMovie
        indexToMovie[idMovie] = movie
        graph.add_node(idMovie, bipartite=1)   # Create node for the movie
        year = extractYear(movie)
        years[year].append(idMovie)
        idMovie = idMovie + 1
    return idMovie   # If the movie is already in the dictionary the id won't change



# Tests

print(extractYear("Risto	Ilmojen ritari: Illu Juutilainen (1996)"))

start_time = time.time()
graph = createGraph("prova.tsv")
#graph = createGraph("imdb-actors-actresses-movies.tsv")
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")
print(graph.number_of_nodes())
print(indexToActor[0])
print(indexToMovie[1])
bruce = actorToIndex['Willis, Bruce']
print(bruce)
print(indexToActor[bruce])
print(years)
print(len(years["2000"]))

