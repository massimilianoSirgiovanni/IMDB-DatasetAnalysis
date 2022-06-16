import networkx as nx
import time

actorToIndex = {}   # Dictionary that return the index of a given actor

indexToActor = {}   # Dictionary that return the actor name for a given index

movieToIndex = {}   # Dictionary that return the index of a given movie

indexToMovie = {}   # Dictionary that return the movie name for a given index

years = {
    '1900': [],
    '1930': [],
    '1940': [],
    '1950': [],
    '1960': [],
    '1970': [],
    '1980': [],
    '1990': [],
    '2000': [],
    '2010': [],
    '2020': []

}



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


def addActor(graph, actor, id):
    # Verify if actor is not in dictionaries, if so the method add it in the dictionary and in the graph
    if actor not in actorToIndex:
        actorToIndex[actor] = id
        indexToActor[id] = actor
        graph.add_node(id, bipartite=0)     # Create node for the actor
        id = id + 1
    return id   # If the actor is already in the dictionary the id won't change

def addMovie(graph, movie, id):
    # Verify if movie is not in dictionaries, if so the method add it in the dictionary and in the graph
    if movie not in movieToIndex:
        movieToIndex[movie] = id
        indexToMovie[id] = movie
        graph.add_node(id, bipartite = 1)   # Create node for the movie
        id = id + 1
    return id   # If the movie is already in the dictionary the id won't change


def extractYear(movie):
    for i in range(0, len(movie)):
        if movie[i] == "(" and movie[i+1] == '2' or movie[i+1] == '1':
            return movie[i+1] + movie[i+2] + movie[i+3] + "0"
    return 0

# Tests

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


