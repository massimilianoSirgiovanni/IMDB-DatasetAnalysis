import networkx as nx
from graphConstruction import indexToActor


# Exercise 3.IV

def actorParticFamousMovies(graph):
    # Searching for the actor who participated in movies with largest number of actors
    maxId = -1    # Variable to store the id of the current max
    currentMax = 0
    for i in indexToActor:  # Iterate on all actors
        neighbors = list(graph.neighbors(i))    # Get the neighbors list for the i-th actor
        sumNeighbor = sumNeighborList(graph, neighbors)  # Obtain the number of actor participating to each movie linked to i
        if sumNeighbor > currentMax:    # Checking for the max value and the correspondent i-th actor
            currentMax = sumNeighbor
            maxId = i
    if maxId > -1:           # Checking if there is no error
        return indexToActor[maxId]
    else:
        print("ERROR: NO ACTOR FOUND IN THE GRAPH")
        return -1

def sumNeighborList(graph, listNodes):
    # Passing a list of nodes, it will return the sum of neighbors of each node
    sum = 0
    for j in listNodes:
        sum = sum + len(list(graph.neighbors(j)))
    return sum


# Exercise 4

def createActorGraph(graph):
    max = (0, 0, 0)     # max[0] = actor1 | max[1] = actor2 | max[2] = the number of collaboration
    # max variable will contain the max number of collaborations and the couple that have made that
    graphActor = nx.Graph()     # Create a new graph for actors
    for i in indexToActor:      # Iteration on all actors
        if graphActor.has_node(i) == False:     # If an actor is not in the graph it will be added as a node
            graphActor.add_node(i)
        tmp = addCollaborators(i, graph, graphActor)  # Add all collaborators of the i-th actor
        if max[2] < tmp[2]:     # Checking for the max value and the correspondent couple of actors
            max = tmp
    return (graphActor, max)    # Return the graph of all actors and the tuple max

def addCollaborators(actor, originalGraph, actorGraph):
    dictEdge = {}   # Dictionary containing the collaborations for "actor"
    movies = originalGraph.neighbors(actor)  # Movies made by "actor"
    maxCollab = (0, 0, 0)   # Flag to store the actor with whom "actor" has done the most collaborations
    for j in movies:    # Iteration on all movies made by "actor"
        actorsInJ = originalGraph.neighbors(j)  # List of actor that have made the j-th movie
        for a in actorsInJ:     # Iteration on actors that have made the j-th movie
            if a > actor:   # If a < actor it mean that a has already been visited and we do not have to reconsider it
                # This if is a consequence of the way we construct the original Graph and how we visit the nodes
                tmp = manageOneCollaboration(actor, a, actorGraph, dictEdge)  # Manage the relation between two actors
                if maxCollab[2] < tmp:  # Checking for the max value and the correspondent couple of actors
                    maxCollab = (actor, a, tmp)
    dictEdge.clear()    # This dictionary is useless for the next actors
    return maxCollab


def manageOneCollaboration(actor1, actor2, actorGraph, dictEdge):
    # Manage a collaboration between two actors
    tmp = 0
    if actorGraph.has_node(actor2) == False:    # If actor2 is not in the graph sure there is no edge (actor1, actor2)
        actorGraph.add_node(actor2)     # actor2 is added to the graph
        actorGraph.add_edge(actor1, actor2)     # is added an edge between actor1 and actor2
        dictEdge[f"({actor1}, {actor2})"] = 1   # It is saved in the dictionary that they are connected
    # If there is the node actor2 there are two possibilities: There is already an edge (actor1, actor2) or there isn't
    elif actorGraph.has_edge(actor1, actor2):
        # The counter in the dictionary is changed
        tmp = dictEdge[f"({actor1}, {actor2})"]
        dictEdge[f"({actor1}, {actor2})"] = tmp + 1     # Update the number of collaborations between the two actors
    else:
        actorGraph.add_edge(actor1, actor2)     # Add an edge between actor1 and actor2
        dictEdge[f"({actor1}, {actor2})"] = 1   # It is saved in the dictionary that they are connected
    return tmp + 1
