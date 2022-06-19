import networkx
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


def actorParticFamousMovies(graph):
    # Searching for the actor who participated in movies with largest number of actors
    max = -1    # Variable to store the id of the current
    sumMax = 0
    for i in indexToActor:  # Iterate on all actors
        neighbors = list(graph.neighbors(i))    # Get the neighbors list for the i-th actor
        sum = sumNeighborList(neighbors)  # Obtain the number of actor participating to each movie linked to i
        if sum > sumMax:    # Checking for the max value and the correspondent actor id
            sumMax = sum
            max = i
    if max > -1:
        return indexToActor[max]
    else:
        print("ERROR: NO ACTOR FOUND IN THE GRAPH")
        return -1

def sumNeighborList(listNodes):
    # Passing a list of nodes, it will return the sum of neighbors of each node
    sum = 0
    for j in listNodes:
        sum = sum + len(list(graph.neighbors(j)))
    return sum

visitNodes = {}

def ecc(nodes, level):
    for i in nodes:
        if i not in visitNodes:
            visitNodes[i] = level
            ecc(graph.neighbors(i), level + 1)
        elif visitNodes[i] > level:
            visitNodes[i] = level
            ecc(graph.neighbors(i), level + 1)
    return 0

# Tests

start_time = time.time()
#graph = createGraph("prova.tsv")
graph = createGraph("imdb-actors-actresses-movies.tsv")
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")
print(graph.number_of_nodes())

print(meanForYear(2030))
print(years[0])

start_time = time.time()
print(actorParticFamousMovies(graph))
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")
'''print(indexToMovie[1967])
print(indexToMovie[18966])
print(indexToMovie[53495])
print(indexToMovie[93776])
print(indexToMovie[123315])'''
'''start_time = time.time()
ecc([0], 0)
end_time = time.time()
print(f"ECCENTRICITY TIME: {end_time-start_time}")
max = 0
for i in visitNodes:
    if visitNodes[i] > max:
        max = visitNodes[i]
print(max)'''
print(networkx.eccentricity(graph, 0))


