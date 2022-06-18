import networkx as nx
import time
from yearsFunctions import *
from pythonds.graphs import Graph, Vertex
from pythonds.basic import Queue


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
        #print(len(list(graph.neighbors(j))))
        sum = sum + len(list(graph.neighbors(j)))
    return sum


def nodeGradeMax(graph):
    max = -1    # Variable to store the id of the current
    sumMax = 0
    selectedActor = 0
    selectedMovie = 0
    
    for i in indexToActor:  # Iterate on all actors
        neighbors = list(graph.neighbors(i))    # Get the neighbors list for the i-th actor
        sum = sumNeighborList(neighbors)  # Obtain the number of actor participating to each movie linked to i
        if sum > sumMax:    # Checking for the max value and the correspondent actor id
            sumMax = sum
            max = i
    
    if max > -1:
        selectedActor = max
    else:
        print("ERROR: NO ACTORS FOUND IN THE GRAPH")
        return -1
    
    
    max = -1
    sumMax = 0
    
    for i in indexToMovie:  # Iterate on all actors
        neighbors = list(graph.neighbors(i))    # Get the neighbors list for the i-th actor
        sum = sumNeighborList(neighbors)  # Obtain the number of actor participating to each movie linked to i
        if sum > sumMax:    # Checking for the max value and the correspondent actor id
            sumMax = sum
            max = i
    
    if max > -1:
        selectedMovie = max
    else:
        print("ERROR: NO MOVIES FOUND IN THE GRAPH")
        return -1
    
    if selectedActor >= selectedMovie:
        return selectedActor
    else:
        return selectedMovie
        
    






"""
def bfs(graph, startNode):
    distance = 0
    pred = -1
    vertQueue = Queue()
    vertQueue.enqueue(startNode)
    while (vertQueue.size() > 0):
        currentVert = vertQueue.dequeue()

    for nbr in currentVert.getConnections():
      if (nbr.getColor() == 'white'):
        nbr.setColor('gray')
        nbr.setDistance(currentVert.getDistance() + 1)
        nbr.setPred(currentVert)
        vertQueue.enqueue(nbr)
    currentVert.setColor('black')


#neighbors = list(graph.neighbors(i))


def bfs(graph, start):
  start.setDistance(0)
  start.setPred(None)
  vertQueue = Queue()
  vertQueue.enqueue(start)
  while (vertQueue.size() > 0):
    currentVert = vertQueue.dequeue()
    for nbr in currentVert.getConnections():
      if (nbr.getColor() == 'white'):
        nbr.setColor('gray')
        nbr.setDistance(currentVert.getDistance() + 1)
        nbr.setPred(currentVert)
        vertQueue.enqueue(nbr)
    currentVert.setColor('black')
"""


def bfs(graph, startNode):
    
    nodeColor = {}
    nodeDistance = {}
    nodePred = {}
    
    visitedNodes = []
    
    # All'inizio tutti i sono nodi white
    for i in graph.nodes():
        nodeColor[i] = "w"
        nodeDistance[i] = 0
        nodePred[i] = None
    
    
    # Inserimento primo vertice
    vertQueue = Queue()
    vertQueue.enqueue(startNode)
    
    
    while vertQueue.size() > 0:
        currentVert = vertQueue.dequeue()
        #neighbors = list(graph.neighbors(startNode))
        neighbors = graph.neighbors(startNode)
        visitedNodes.append(currentVert)
        
        
        for nbr in neighbors:
            if nodeColor[nbr] == 'w':
                nodeColor[nbr] = 'g' # Colore grigio
                nodeDistance[nbr] = nodeDistance[nbr] + 1
                nodePred[nbr] = currentVert
                vertQueue.enqueue(nbr)
        nodeColor[currentVert] = 'b' # Colore nero
    print("BFS: ", visitedNodes, "Distanza: ")
    #print("BFS: ", vertQueue, "Distanza: ")
    # Il risultato è della forma: [nodo attuale, vicino1, vicino2, ...]
    
    #1 VA DEFINITO IL VALORE DELL'ECCENTRICITà
    #2 PROBABILMENTE LA LISTA DEI NODI VISITATI VA RIEMPITA IN UNA PARTE DIVERSA DA DOVE HO SCRITTO IO L'ISTRUZIONE
    #3 ANDREBBE STAMPATO visitedNodes MA VA TROVATA LA FUNZIONE
    
    
def graphDiameter(graph, startIndexNode):
    lb = bfs(graph, startIndexNode)
    
    
    
    #for i in graph:




    return 0
    
    
    
    
    
    
    
    """
    actualDistance = 0
    
    startNode.setDistance(0)
    startNode.setPred(None)
    vertQueue = Queue()
    vertQueue.enqueue(startNode)

    while vertQueue.size() > 0:
        currentVert = vertQueue.dequeue()
        neighbors = graph.neighbors(startNode)

        for nbr in neighbors:
            if nbr.getColor() == 'white':
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance() + 1)
                nbr.setPred(currentVert)
                vertQueue.enqueue(nbr)
        currentVert.setColor('black')
"""

# Tests

#print(extractYear("Risto	Ilmojen ritari: Illu Juutilainen (1996)"))


start_time = time.time()
graph = createGraph("prova.tsv")
#graph = createGraph("imdb-actors-actresses-movies.tsv")
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")

print("Grafo ", graph)


#################################
############## BFS ##############
#################################


# Test BFS sui primi 20 nodi:
for k in range(20):
    bfs(graph, k)


#print(graphDiameter(graph, 3))



#print(graph.number_of_nodes())

#print(meanForYear(2000))
#print(meanForYear(2030))
#print(years[0])








# Ese 3.4

start_time = time.time()
print(actorParticFamousMovies(graph))
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")


"""
print(indexToMovie[1967])
print(indexToMovie[18966])
print(indexToMovie[53495])
print(indexToMovie[93776])
print(indexToMovie[123315])
"""



