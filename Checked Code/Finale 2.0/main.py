import networkx as nx
import time
from yearsFunctions import *
from diameterEvaluation import *


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
        year = extractYear(textLine[1])
        index = addActor(graph, textLine[0], index, year)
        index = addMovie(graph, textLine[1], index, year)
        graph.add_edge(actorToIndex[textLine[0]], movieToIndex[textLine[1]])    # Add an edge between actor and movie
    file.close()
    return graph


def addActor(graph, actor, idActor, year):
    # Verify if actor is not in dictionaries, if so the method add it in the dictionary and in the graph
    if actor not in actorToIndex:
        actorToIndex[actor] = idActor
        indexToActor[idActor] = actor
        graph.add_node(idActor, bipartite=0)     # Create node for the actor
        if idActor not in yearsActor[year]:
            yearsActor[year].add(idActor)
        idActor = idActor + 1
    return idActor   # If the actor is already in the dictionary the id won't change

def addMovie(graph, movie, idMovie, year):
    # Verify if movie is not in dictionaries, if so the method add it in the dictionary and in the graph
    if movie not in movieToIndex:
        movieToIndex[movie] = idMovie
        indexToMovie[idMovie] = movie
        graph.add_node(idMovie, bipartite=1)   # Create node for the movie
        years[year].add(idMovie)
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


###############################################





#############################################################################


'''def createActorGraphD():
    dictActors = {}
    max = (0, 0, 0)
    for i in indexToActor:
        if i not in dictActors:
            dictActors[i] = set(graph.neighbors(i))
        for j in indexToActor:
            if j != i:
                if j not in dictActors:
                    dictActors[j] = set(graph.neighbors(j))
                intersect = dictActors[i] & (dictActors[j])
                if len(intersect) > max[2]:
                    max = (i, j, len(intersect))
    return max'''


def createActorGraph():
    max = (0, 0, 0)
    G = nx.Graph()
    visitedNodes = {}
    for i in indexToActor:
        if G.has_node(i) == False:
            G.add_node(i)
        tmp = addCollaborators(G, i, visitedNodes)
        visitedNodes[i] = 0
        if max[2] < tmp[2]:
            max = tmp
    return (G, max)

def addCollaborators(actorGraph, actor, visitedNodes):
    dictEdge = {}
    movies = graph.neighbors(actor)
    max = (0, 0, 0)
    for j in movies:
        actors = graph.neighbors(j)
        for p in actors:
            if p != actor:
                tmp = 0
                if p not in visitedNodes:
                    if actorGraph.has_node(p) == False:
                        actorGraph.add_node(p)
                        actorGraph.add_edge(actor, p)
                        dictEdge[f"({actor}, {p})"] = 1
                    elif actorGraph.has_edge(actor, p):
                        if f"({actor}, {p})" in dictEdge:
                            tmp = dictEdge[f"({actor}, {p})"]
                            dictEdge[f"({actor}, {p})"] = tmp + 1
                        else:
                            tmp = dictEdge[f"({p}, {actor})"]
                            dictEdge[f"({p}, {actor})"] = tmp + 1
                    else:
                        actorGraph.add_edge(actor, p)
                        dictEdge[f"({actor}, {p})"] = 1
                    if max[2] < tmp + 1:
                        max = (actor, p, tmp + 1)
    #print(dictEdge)
    return max

'''def createActorGraphMovie():
    max = (0, 0, 0)
    dictEdge = {}
    actorGraph = nx.Graph()
    for movie in indexToMovie:
        tmp = linkActorsFromMovie(actorGraph, movie, dictEdge)
        if max[2] < tmp[2]:
            max = tmp
    print(dictEdge)
    return (actorGraph, max)
def linkActorsFromMovie(actorGraph, movie, dictEdge):
    max = (0, 0, 0)
    actors = list(graph.neighbors(movie))
    for i in range(0, len(actors)):
        if actorGraph.has_node(actors[i]) == False:
            actorGraph.add_node(actors[i])
        for j in range(i + 1, len(actors)):
            tmp = 0
            if actorGraph.has_node(actors[j]) == False:
                actorGraph.add_node(actors[j])
                actorGraph.add_edge(actors[i], actors[j])
                dictEdge[f"({actors[i]}, {actors[j]})"] = 1
            elif actorGraph.has_edge(actors[i], actors[j]) == False:
              #  tmp = actorGraph[actors[i]][actors[j]]['weight']
             #   actorGraph[actors[i]][actors[j]]['weight'] = tmp + 1
            #else:
                actorGraph.add_edge(actors[i], actors[j])
                dictEdge[f"({actors[i]}, {actors[j]})"] = 1
            else:
                if f"({actors[i]}, {actors[j]})" in dictEdge:
                    tmp = dictEdge[f"({actors[i]}, {actors[j]})"]
                    dictEdge[f"({actors[i]}, {actors[j]})"] = tmp + 1
                else:
                    tmp = dictEdge[f"({actors[j]}, {actors[i]})"]
                    dictEdge[f"({actors[j]}, {actors[i]})"] = tmp + 1
            if max[2] < tmp + 1:
                max = (actors[i], actors[j], tmp + 1)
    return max'''

# IMPLEMENTAZIONE SOVRASCRITTURA DEL GRAFO

'''def createActorGraphMovie(graph):
    max = (0, 0, 0)
    dictEdge = {}
    for movie in indexToMovie:
        tmp = linkActorsFromMovie(graph, movie, dictEdge)
        if max[2] < tmp[2]:
            max = tmp
    return (graph, max)
def linkActorsFromMovie(graph, movie, dictEdge):
    max = (0, 0, 0)
    actors = list(graph.neighbors(movie))
    graph.remove_node(movie)
    for i in range(0, len(actors)):
        for j in range(i + 1, len(actors)):
            tmp = 0
            if graph.has_edge(actors[i], actors[j]) == False:
                graph.add_edge(actors[i], actors[j])
                dictEdge[f"({actors[i]}, {actors[j]})"] = 1
            else:
                if f"({actors[i]}, {actors[j]})" in dictEdge:
                    tmp = dictEdge[f"({actors[i]}, {actors[j]})"]
                    dictEdge[f"({actors[i]}, {actors[j]})"] = tmp + 1
                else:
                    tmp = dictEdge[f"({actors[j]}, {actors[i]})"]
                    dictEdge[f"({actors[j]}, {actors[i]})"] = tmp + 1
            if max[2] < tmp + 1:
                max = (actors[i], actors[j], tmp + 1)
    return max'''


#############################################################################

# Tests

start_time = time.time()
#graph = createGraph("prova.tsv")
graph = createGraph("imdb-actors-actresses-movies.tsv")
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")
print(graph)
'''print(meanForYear(2020))
print(years[0])'''

'''start_time = time.time()
print(actorParticFamousMovies(graph))
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")
''''''print(indexToMovie[1967])
print(indexToMovie[18966])
print(indexToMovie[53495])
print(indexToMovie[93776])
print(indexToMovie[123315])'''

'''x = 2020
start_time = time.time()
diameter = diameterUpToYear(x, graph)
print(f"The Diameter is: {diameter}")'''


'''setYear = createGraphUpToYear(x, graph)
end_time = time.time()
print(f"EXECUTION TIME: {end_time - start_time}")
start_time = time.time()
maxGrade = nodeGradeMax(graph, setYear)
if maxGrade in indexToActor:
    print(indexToActor[maxGrade])
end_time = time.time()
print(f"EXECUTION TIME: {end_time - start_time}")
doubSwNode = doubleSweep(graph, maxGrade, setYear)
print(doubSwNode)
start_time = time.time()
diameter = diameter(graph, doubSwNode, setYear)
print(f"The Diameter is: {diameter}")
#print(f"Ecc con metodo nostro: {eccentricity(graphYear, list(graphYear.nodes)[0])[0]}")
end_time = time.time()
print(f"EXECUTION TIME: {end_time - start_time}")'''



'''start_time = time.time()
print(f"Ecc con metodo networkX: {nx.eccentricity(graphYear, list(graphYear.nodes)[0])}")
end_time = time.time()
print(f"EXECUTION TIME: {end_time - start_time}")'''


start_time = time.time()
graph2 = createActorGraph()
end_time = time.time()
print(graph2[0])
print(f"Gli attori che hanno collaborato maggiormente sono: {indexToActor[graph2[1][0]]} e {indexToActor[graph2[1][1]]}")
print(f"Hanno collaborato {graph2[1][2]} volte")

print(f"EXECUTION TIME: {end_time - start_time}")


'''start_time = time.time()
graph3 = createActorGraphMovie(graph)
end_time = time.time()
print(graph3[0])
print(f"Gli attori che hanno collaborato maggiormente sono: {indexToActor[graph3[1][0]]} e {indexToActor[graph3[1][1]]}")
print(f"Hanno collaborato {graph3[1][2]} volte")
print(f"EXECUTION TIME: {end_time - start_time}")'''

print(graph)