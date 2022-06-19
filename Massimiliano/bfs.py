import networkx as nx
import time
from yearsFunctions import *
from pythonds.basic import Queue
from queueOur import *

actorToIndex = {}  # Dictionary that return the index of a given actor

indexToActor = {}  # Dictionary that return the actor name for a given index

movieToIndex = {}  # Dictionary that return the index of a given movie

indexToMovie = {}  # Dictionary that return the movie name for a given index


def createGraph(fileName):
    file = open(fileName, "r")  # Open file
    index = 0  # Index link to actors and movies
    graph = nx.Graph()  # Graph Initialization
    for line in file:  # Scan the file line by line
        textLine = line.rstrip('\n').split('\t')  # Insert the couple (actor, movie) in a variable
        index = addActor(graph, textLine[0], index)
        index = addMovie(graph, textLine[1], index)
        graph.add_edge(actorToIndex[textLine[0]], movieToIndex[textLine[1]])  # Add an edge between actor and movie
    file.close()
    return graph


def addActor(graph, actor, idActor):
    # Verify if actor is not in dictionaries, if so the method add it in the dictionary and in the graph
    if actor not in actorToIndex:
        actorToIndex[actor] = idActor
        indexToActor[idActor] = actor
        graph.add_node(idActor, bipartite=0)  # Create node for the actor
        idActor = idActor + 1
    return idActor  # If the actor is already in the dictionary the id won't change


def addMovie(graph, movie, idMovie):
    # Verify if movie is not in dictionaries, if so the method add it in the dictionary and in the graph
    if movie not in movieToIndex:
        movieToIndex[movie] = idMovie
        indexToMovie[idMovie] = movie
        graph.add_node(idMovie, bipartite=1)  # Create node for the movie
        year = extractYear(movie)
        years[year].append(idMovie)
        idMovie = idMovie + 1
    return idMovie  # If the movie is already in the dictionary the id won't change


def actorParticFamousMovies(graph):
    # Searching for the actor who participated in movies with largest number of actors
    max = -1  # Variable to store the id of the current
    sumMax = 0
    for i in indexToActor:  # Iterate on all actors
        neighbors = list(graph.neighbors(i))  # Get the neighbors list for the i-th actor
        sum = sumNeighborList(neighbors)  # Obtain the number of actor participating to each movie linked to i
        if sum > sumMax:  # Checking for the max value and the correspondent actor id
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
        # print(len(list(graph.neighbors(j))))
        sum = sum + len(list(graph.neighbors(j)))
    return sum


def nodeGradeMax(graph):
    maxN = -1  # Variable to store the id of the current
    sumMax = 0
    selectedActor = 0
    selectedMovie = 0
    actorNeighbors = 0
    movieNeighbors = 0

    for i in indexToActor:
        neighbors = list(graph.neighbors(i))
        sumN = len(neighbors)
        if sumN > sumMax:
            sumMax = sumN
            maxN = i

    if maxN > -1:
        selectedActor = maxN  # Attore con più vicini
        actorNeighbors = sumMax  # Numero di vicini dell'attore
    else:
        print("ERROR: NO ACTORS FOUND IN THE GRAPH")
        return -1

    maxN = -1
    sumMax = 0

    for i in indexToMovie:
        neighbors = list(graph.neighbors(i))
        sumN = len(neighbors)
        if sumN > sumMax:
            sumMax = sumN
            maxN = i

    if maxN > -1:
        selectedMovie = maxN  # Attore con più vicini
        movieNeighbors = sumMax  # Numero di vicini dell'attore
    else:
        print("ERROR: NO ACTORS FOUND IN THE GRAPH")
        return -1

    if actorNeighbors >= movieNeighbors:
        return selectedActor
    else:
        return selectedMovie


def bfs(graph, startNode):
    #nodeColor = {}
    nodeDistance = {}

    nodeColor = {node: "w" for node in graph.nodes()}

    # visitedNodes = []

    # All'inizio tutti i nodi sono white, distanza 0 e nessun predecessore

    # Inserimento primo vertice
    # vertQueue = Queue()
    # vertQueue.enqueue(startNode)
    max = 0

    for currentVert in nodeColor:
        # currentVert = vertQueue.dequeue()
        if currentVert not in nodeDistance:
            nodeDistance[currentVert] = 0
        neighbors = list(graph.neighbors(currentVert))

        for nbr in neighbors:
            #if nbr not in nodeDistance:
            if nodeColor[nbr] == "w":
                nodeColor[nbr] = 'g'  # Colore grigio
                nodeDistance[nbr] = nodeDistance[currentVert] + 1
                if nodeDistance[nbr] > max:
                    max = nodeDistance[nbr]
                #vertQueue.enqueue(nbr)
        nodeColor[currentVert] = 'b'  # Colore nero

    # print("Dizionario distanze: ", nodeDistance)
    return max


# Calcolo dell'eccentricità
def eccentricity(graph, startNode):
    max = bfs(graph, startNode)
    return max

    # print("BFS: ", visitedNodes, "Distanza: ")
    # print("BFS: ", vertQueue, "Distanza: ")
    # Il risultato è della forma: [nodo attuale, vicino1, vicino2, ...]

    # 1 VA DEFINITO IL VALORE DELL'ECCENTRICITà
    # 2 PROBABILMENTE LA LISTA DEI NODI VISITATI VA RIEMPITA IN UNA PARTE DIVERSA DA DOVE HO SCRITTO IO L'ISTRUZIONE
    # 3 ANDREBBE STAMPATO visitedNodes MA VA TROVATA LA FUNZIONE


def graphDiameter(graph, startIndexNode):
    lb = bfs(graph, startIndexNode)

    # for i in graph:

    return 0


# Tests

# print(extractYear("Risto	Ilmojen ritari: Illu Juutilainen (1996)"))


start_time = time.time()
graph = createGraph("prova.tsv")
#graph = createGraph("imdb-actors-actresses-movies.tsv")
end_time = time.time()
print(f"EXECUTION TIME: {end_time - start_time}")

# print("Grafo ", graph)


#################################
############## BFS ##############
#################################


# print("Nodo di grado massimo: ", nodeGradeMax(graph))



# bfs(graph, 0)


'''maxGradeNode = nodeGradeMax(graph)
if maxGradeNode not in indexToMovie:
    print(indexToActor[maxGradeNode])
else:
    print(indexToMovie[maxGradeNode])'''
start_time = time.time()
print("Valore eccentricità: ", eccentricity(graph, 0))
end_time = time.time()
print(f"EXECUTION TIME: {end_time - start_time}")

# Test BFS sui primi 20 nodi:
# for k in range(20):
#   bfs(graph, k)


# print(graphDiameter(graph, 3))


# print(graph.number_of_nodes())

# print(meanForYear(2000))
# print(meanForYear(2030))
# print(years[0])


# Ese 3.4

'''start_time = time.time()
print(actorParticFamousMovies(graph))
end_time = time.time()
print(f"EXECUTION TIME: {end_time - start_time}")'''

"""
print(indexToMovie[1967])
print(indexToMovie[18966])
print(indexToMovie[53495])
print(indexToMovie[93776])
print(indexToMovie[123315])
"""

