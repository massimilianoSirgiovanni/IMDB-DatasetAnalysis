import networkx as nx
from yearsFunctions import yearsMovie, yearsActor, extractYear

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
        index = addTupleActorMovie(graph, textLine, index)   # Insert the couple (actor, movie) in dictionaries and in graph
        graph.add_edge(actorToIndex[textLine[0]], movieToIndex[textLine[1]])    # Add an edge between actor and movie
    file.close()
    return graph


def addTupleActorMovie(graph, textLine, index):
    year = extractYear(textLine[1])     # Extract the release year of the current movie
    index = addActor(graph, textLine[0], index, year)   # Add the actor in the dictionaries and graph
    index = addMovie(graph, textLine[1], index, year)   # Add the actor in the dictionaries and graph
    return index    # Return the current index (maybe it can be the same as the argument)

def addActor(graph, actor, idActor, year):
    # Verify if actor is not in dictionaries, if so the method add it in the dictionary and in the graph
    if actor not in actorToIndex:
        actorToIndex[actor] = idActor   # Actor added in dictionaries
        indexToActor[idActor] = actor
        graph.add_node(idActor, bipartite=0)     # Create node for the actor
        idActor = idActor + 1
    if actorToIndex[actor] not in yearsActor[year]:  # Add actor in years dictionary
        yearsActor[year].add(actorToIndex[actor])
    return idActor   # If the actor is already in the dictionary the id won't change

def addMovie(graph, movie, idMovie, year):
    # Verify if movie is not in dictionaries, if so the method add it in the dictionary and in the graph
    if movie not in movieToIndex:
        movieToIndex[movie] = idMovie     # Movie added in dictionaries
        indexToMovie[idMovie] = movie
        graph.add_node(idMovie, bipartite=1)    # Create node for the movie
        yearsMovie[year].add(idMovie)                # Add actor in years dictionary
        idMovie = idMovie + 1
    return idMovie   # If the movie is already in the dictionary the id won't change