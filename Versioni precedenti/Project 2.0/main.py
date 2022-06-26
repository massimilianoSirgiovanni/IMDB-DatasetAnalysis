import networkx as nx
import time
from yearsFunctions import *
from diameterEvaluation import *
#from diameter2 import *


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


dictActor = {}

def createActorGraph():
    max = (0, 0, 0)
    G = nx.Graph()
    for i in indexToActor:
        if i not in dictActor:
            dictActor[i] = 0
            G.add_node(i)
        tmp = addCollaborators(G, i)
        if max[2] < tmp[2]:
            max = tmp
    max = (max[0], max[1], max[2]/2)
    return (G, max)

def addCollaborators(G, actor):
    movies = graph.neighbors(actor)
    max = (0, 0, 0)
    for j in movies:
        actors = graph.neighbors(j)
        for p in actors:
            if p != actor:
                if p not in dictActor:
                    dictActor[p] = 0
                    G.add_node(p)
                    G.add_edge(actor, p, weight=1)
                elif G.has_edge(actor, p):
                    G[actor][p]['weight'] = G[actor][p]['weight'] + 1
                    if max[2] < G[actor][p]['weight']:
                        max = (actor, p, G[actor][p]['weight'])
                else:
                    G.add_edge(actor, p, weight=1)

    return max

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

x = 1990
start_time = time.time()
diameter = diameterUpToYear(1920, graph)
print(f"The Diameter is: {diameter}")


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



'''start_time = time.time()
graph2 = createActorGraph()
end_time = time.time()
print(f"Gli attori che hanno collaborato maggiormente sono: {indexToActor[graph2[1][0]]} e {indexToActor[graph2[1][1]]}")
print(f"Hanno collaborato {graph2[1][2]} volte")

print(f"EXECUTION TIME: {end_time - start_time}")'''



