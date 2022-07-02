# A RAM of 16GB or higher is recommended for running

import random
from math import floor
import time
import networkx as nx


actorToIndex = {}   # Dictionary that return the index of a given actor

indexToActor = {}   # Dictionary that return the actor name for a given index

movieToIndex = {}   # Dictionary that return the index of a given movie

indexToMovie = {}   # Dictionary that return the movie name for a given index


# Dictionary for movies

lbYears = 1880      # Lower bound for the set of possible x (Cannot go below 1880 unless the dictionaries are changed)
ubYears = 2020      # Upper bound for the set of possible x (Cannot go above 2020 unless the dictionaries are changed)

yearsMovie = {
    0: set(),  # Errors in data
    1870: set(),  # [1880, 1880]
    1880: set(),  # (1880, 1890]
    1890: set(),  # (1890, 1900]
    1900: set(),  # (1890, 1910]
    1910: set(),  # (1910, 1920]
    1920: set(),  # (1920, 1930]
    1930: set(),  # (1930, 1940]
    1940: set(),  # (1940, 1950]
    1950: set(),  # (1950, 1960]
    1960: set(),  # (1960, 1970]
    1970: set(),  # (1970, 1980]
    1980: set(),  # (1980, 1990]
    1990: set(),  # (1990, 2000]
    2000: set(),  # (2000, 2010]
    2010: set(),  # (2010, 2020]

}

# Dictionary for actors
yearsActor = {
    0: set(),  # Errors in data
    1870: set(),  # [1880, 1880]
    1880: set(),  # (1880, 1890]
    1890: set(),  # (1890, 1900]
    1900: set(),  # (1890, 1910]
    1910: set(),  # (1910, 1920]
    1920: set(),  # (1920, 1930]
    1930: set(),  # (1930, 1940]
    1940: set(),  # (1940, 1950]
    1950: set(),  # (1950, 1960]
    1960: set(),  # (1960, 1970]
    1970: set(),  # (1970, 1980]
    1980: set(),  # (1980, 1990]
    1990: set(),  # (1990, 2000]
    2000: set(),  # (2000, 2010]
    2010: set(),  # (2010, 2020]

}



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
    yearsActor[year].add(actorToIndex[actor])  # Add actor in years dictionary
    return idActor   # If the actor is already in the dictionary the id won't change

def addMovie(graph, movie, idMovie, year):
    # Verify if movie is not in dictionaries, if so the method add it in the dictionary and in the graph
    if movie not in movieToIndex:
        movieToIndex[movie] = idMovie     # Movie added in dictionaries
        indexToMovie[idMovie] = movie
        graph.add_node(idMovie, bipartite=1)    # Create node for the movie
        yearsMovie[year].add(idMovie)                # Add movie in years dictionary
        idMovie = idMovie + 1
    return idMovie   # If the movie is already in the dictionary the id won't change



def extractYear(movie):
    # Function for extracting the year from each line of the file

    for i in range(len(movie) - 6, -1, -1):  # Start from the tail of the string because the year is always after the name

        if movie[i] == "(" and (
                movie[i + 1] == '2' or movie[i + 1] == '1'):  # Checking from the "(" to avoid situation like: (2003/II)
            year = int(movie[i + 1] + movie[i + 2] + movie[i + 3] + movie[i + 4])

            if movie[i + 4] == "0":
                return year - 10

            return year - (year % 10)  # Return an integer with the decade of the movie

    return 0


# Exercise 1.F

def averageForYear(x):
    # Function for the average number of movies per year up to year x

    x, yearSum, n = averageChecks(x)  # Preliminary checks
    if n == 0 and x == 1880:                          # In the dictionary at 1870 label there is only one year
        yearSum = len(yearsMovie[lbYears - 10])
        n = 1

    # Calculation of the components for the average
    while x > lbYears:
        x = x - 10
        n = n + 10
        yearSum = yearSum + len(yearsMovie[x])

    return yearSum / n  # Calculation of the average


def averageChecks(x):
    # Preliminary checks for the selected year x.
    # It must be a value between lbYears and ubYears

    if type(x) is str:
        x = int(x)

    if x < lbYears - 10:
        return 0, 0, 1

    if x >= ubYears + 10:
        print("ERROR: You can not insert a year over 2020")
        return 0, 0, 1

    if (x % 10) != 0:
        tmp = x
        x = x - (x % 10)  # Calculation of the year's decade
        print(f"ATTENTION: The year {tmp} is not a decade so it was transformed to {x}")

    return x, 0, 0


# Function useful for Exercise 2.1
def createSetUpToYear(x):
    # Creation of a common set that contains movies and actors up to the year x

    x = averageChecks(x)[0]  # Preliminary checks
    unionSet = set()  # Creation of the set

    while x >= lbYears:  # Initialization of the set
        x = x - 10
        unionSet = unionSet.union(yearsMovie[x])
        unionSet = unionSet.union(yearsActor[x])

    return unionSet


# Exercise 2.1

def diameterUpToYear(x, graph):
    # Diameter up to the selected year x

    setConsideredNodes = createSetUpToYear(x)  # Common set for movies and actors

    # Find the node with maximum grade in the biggest connected component
    if len(setConsideredNodes) == 0:
        print(f"ATTENTION: There are no movies up to the year {x}")
        return 0
    maxGrade = nodeWithMaxDegree(graph, setConsideredNodes)

    # Use the 2-Sweep algorithm starting from the node with max grade
    startEcc = doubleSweep(graph, maxGrade, setConsideredNodes)

    # Diameter evaluation
    diam = diameter(graph, startEcc, setConsideredNodes)
    return diam


def nodeWithMaxDegree(graph, consideredNodes):
    # Function that searches for the node with maximum degree

    maxNode = -1  # Variable to store the id of the current node
    maxDegree = 0  # Variable to store the current max degree
    giant = max(nx.connected_components(graph.subgraph(consideredNodes)), key=len)  # Finds largest connected component

    # For all nodes in biggestComponent connected component we search the node with maximum grade
    for i in giant:
        degreeNode = graph.degree(i)  # the degree() function is from NetworkX

        if degreeNode > maxDegree:  # Update of the node of maximum degree
            maxDegree = degreeNode
            maxNode = i

    if maxNode == -1:  # Empty graph case
        print("ERROR: NO NODE FOUND IN THE GRAPH")
        return -1

    else:
        return maxNode  # Node with maximum degree


def doubleSweep(graph, startNode, setConsideredNodes):
    # 2-Sweep procedure

    startingEcc = bfs(graph, startNode, setConsideredNodes, fringeReturn=1)  # Eccentricity of the starting node

    dSweepDiameter = bfs(graph, startingEcc[1][startingEcc[0]][0], setConsideredNodes, pathsReturn=1)  # calculation of the diameter

    return combinedChoice(dSweepDiameter, startingEcc, graph, setConsideredNodes)

def combinedChoice(dSweepDiameter, gradeMaxEcc, graph, setConsideredNodes):
    # Method linked to the doubleSweep() function
    centralNode = floor(dSweepDiameter[0] / 2)  # The midpoint is found
    minEcc = gradeMaxEcc
    lefts = len(dSweepDiameter[2])
    visitedNodes = {}
    for i in dSweepDiameter[2]:
        if i[centralNode] not in visitedNodes:
            visitedNodes[i[centralNode]] = 0
            centerNodeEcc = bfs(graph, i[centralNode], setConsideredNodes, fringeReturn=1)
            if minEcc[0] > centerNodeEcc[0] or \
                    (minEcc[0] == centerNodeEcc[0] and len(centerNodeEcc[1][centerNodeEcc[0]]) < len(minEcc[1][minEcc[0]])):
                minEcc = centerNodeEcc
        lefts = lefts - 1
        if lefts > len(minEcc[1][minEcc[0]]):
            return minEcc

    return minEcc


def bfs(graph, startNode, setConsideredNodes=0, fringeReturn=0, pathsReturn=0):
    # Bfs algorithm to find the eccentricity of a node
    if setConsideredNodes == 0:
        setConsideredNodes = set(graph.nodes)

    eccPath = {startNode: [startNode]}
    fringes = {}  # To save all Fi for i in [1,..., eccentricity] (dictionary of lists)

    nodeToDistance = {startNode: 0}  # To memorize distance of nodes

    nodeToVisit = [startNode]
    index = 0
    actualMaxDistance = 0

    # Until we have visited all the nodes
    while index < len(nodeToVisit):
        currentVert = nodeToVisit[index]
        neighbors = list(graph.neighbors(currentVert))

        for nbr in neighbors:

            if nbr in setConsideredNodes:  # if nbr had the property of the set
                if nbr not in nodeToDistance:  # if the node is white

                    # In this case we add nbr to the nodes path
                    if pathsReturn == 1:    # In this case the paths are calculated
                        eccPath[nbr] = eccPath[currentVert].copy()
                        eccPath[nbr].append(nbr)
                    nodeToVisit.append(nbr)    # the nodes become gray
                    nodeToDistance[nbr] = nodeToDistance[currentVert] + 1

                    if fringeReturn == 1:   # In this case the fringe is calculated
                        # Add nbr to distanceToNodes
                        if nodeToDistance[nbr] not in fringes:
                            # Create a list for nodes that have nodeToDistance[nbr] distance
                            fringes[nodeToDistance[nbr]] = [nbr]
                        else:
                            # the node will be insert in the fringe at distance nodeToDistance[nbr]
                            fringes[nodeToDistance[nbr]].append(nbr)

                    # Update of maximum distance
                    if nodeToDistance[nbr] > actualMaxDistance:
                        actualMaxDistance = nodeToDistance[nbr]

        index = index + 1  # the nodes become black
    if pathsReturn == 1:
        return (actualMaxDistance, fringes, searchPathsAtGivenDistance(eccPath, actualMaxDistance))

    return (actualMaxDistance, fringes)


def searchPathsAtGivenDistance(dictDistances, distance):
    # Select the paths having input distance from the dictionary
    paths = []
    for i in dictDistances:
        if len(dictDistances[i]) - 1 == distance:
            paths.append(dictDistances[i])

    return paths


def eccentricity(graph, startNode, setConsideredNodes):
    # Calculation of eccentricity
    return bfs(graph, startNode, setConsideredNodes)    # Standard version of bfs without fringe and paths return flags


def eccBi(graph, nodeList, setConsideredNodes, lb):
    # Maximum eccentricity of nodes in the level i
    maxBi = lb
    for node in nodeList:
        actualBiDistance = eccentricity(graph, node, setConsideredNodes)
        # Selection of max{lb, Bi(u)}
        if actualBiDistance[0] > maxBi:
            maxBi = actualBiDistance[0]

    return maxBi


def diameter(graph, startEcc, setConsideredNodes):
    # Diameter of a connected component

    i = startEcc[0]  # Eccentricity of starting node
    lb = i
    ub = 2 * lb

    while ub > lb:
        start_time = time.time()
        bi = eccBi(graph, startEcc[1][i], setConsideredNodes, lb)  # max{lb, Bi(u)}
        end_time = time.time()
        print(f"Bi() at {i} level TIME: {end_time - start_time}: with {bi}")
        lb = bi

        if lb > 2 * (i - 1):  # Stop condition
            return lb

        ub = 2 * (i - 1)
        i = i - 1

    return lb


# Exercise 3.IV

def actorParticipatingFamousMovies(graph):
    # Searching for the actor who participated in movies with largest number of actors
    maxId = -1  # Variable to store the id of the current max
    currentMax = 0
    for actor in indexToActor:  # Iterate on all actors
        neighbors = list(graph.neighbors(actor))  # Get the neighbors list for the i-th actor
        sumNeighbor = sumNeighborList(graph,
                                      neighbors)  # Obtain the number of actor participating to each movie linked to i
        if sumNeighbor > currentMax:  # Checking for the max value and the correspondent i-th actor
            currentMax = sumNeighbor
            maxId = actor
    if maxId > -1:  # Checking if there is no error
        return indexToActor[maxId]
    else:
        print("ERROR: NO ACTOR FOUND IN THE GRAPH")
        return -1


def sumNeighborList(graph, listNodes):
    # Passing a list of nodes, it will return the sum of neighbors of each node
    sumActors = 0
    for movie in listNodes:
        sumActors = sumActors + len(list(graph.neighbors(movie)))
    return sumActors


# Exercise 4

def createActorGraph(graph):
    # Creation of actors (collaborators) graph

    maxCollab = (0, 0, 0)  # max[0] = actor1 | max[1] = actor2 | max[2] = the number of collaboration
    # max variable will contain the max number of collaborations and the couple that have made that
    graphActor = nx.Graph()  # Create a new graph for actors

    for actor in indexToActor:  # Iteration on all actors
        if graphActor.has_node(actor) == False:  # If an actor is not in the graph it will be added as a node
            graphActor.add_node(actor)

        tmp = addCollaborators(actor, graph, graphActor)  # Add all collaborators of the i-th actor

        if maxCollab[2] < tmp[2]:  # Checking for the max value and the correspondent couple of actors
            maxCollab = tmp
    return (graphActor, maxCollab)  # Return the graph of all actors and the tuple max


def addCollaborators(actor, originalGraph, actorGraph):
    # Manage collaborators of "actor"

    dictEdge = {}  # Dictionary containing the collaborations for "actor"
    movies = originalGraph.neighbors(actor)  # Movies made by "actor"
    maxCollab = (0, 0, 0)  # Flag to store the actor with whom "actor" has done the most collaborations

    for movie in movies:  # Iteration on all movies made by "actor"
        actorsInMovie = originalGraph.neighbors(movie)  # List of actor that have made the j-th movie

        for a in actorsInMovie:  # Iteration on actors that have made the j-th movie

            if a > actor:  # If a < actor it mean that "a" has already been visited and we do not have to reconsider it
                # This if is a consequence of the way we construct the original Graph and how we visit the nodes
                tmp = manageOneCollaboration(actor, a, actorGraph, dictEdge)  # Manage the relation between two actors

                if maxCollab[2] < tmp:  # Checking for the max value and the correspondent couple of actors
                    maxCollab = (actor, a, tmp)

    # This dictEdge istance is useless for the next actors
    return maxCollab


def manageOneCollaboration(actor1, actor2, actorGraph, dictEdge):
    # Manage a collaboration between two actors

    tmp = 0

    if actorGraph.has_node(actor2) == False:  # If actor2 is not in the graph sure there is no edge (actor1, actor2)
        actorGraph.add_node(actor2)  # actor2 is added to the graph
        actorGraph.add_edge(actor1, actor2)  # is added an edge between actor1 and actor2
        dictEdge[f"({actor1}, {actor2})"] = 1  # It is saved in the dictionary that they are connected


    # If there is the node actor2 there are two possibilities:
    # There is already an edge (actor1, actor2) or there isn't
    elif actorGraph.has_edge(actor1, actor2):
        # The counter in the dictionary is changed
        tmp = dictEdge[f"({actor1}, {actor2})"]
        dictEdge[f"({actor1}, {actor2})"] = tmp + 1  # Update the number of collaborations between the two actors
    else:
        actorGraph.add_edge(actor1, actor2)  # Add an edge between actor1 and actor2
        dictEdge[f"({actor1}, {actor2})"] = 1  # It is saved in the dictionary that they are connected

    return tmp + 1


# EXECUTION OUTPUT

print("-------START EXECUTION-------\n")
print("0) GRAPH CONSTRUCTION --------------------------------------------------------------------------\n")
start_time = time.time()
graphImbd = createGraph("imdb-actors-actresses-movies.tsv")
print(graphImbd)
construction_time = time.time()
print(f"CONSTRUCTION TIME: {construction_time - start_time}\n")

search_start_time = time.time()
selected = random.randint(0, len(graphImbd.nodes) - 1)
if selected in indexToActor:
    print(f"The node randomly selected is {selected} and it corresponding to the actor {indexToActor[selected]}\n")
else:
    print(f"The node randomly selected is {selected} and it corresponding to the movie {indexToMovie[selected]}\n")
print(f"The actor Bruce Willis correspond to the node {actorToIndex['Willis, Bruce']}")
print(f"Verify: Actor for node {actorToIndex['Willis, Bruce']} --> {indexToActor[actorToIndex['Willis, Bruce']]}")
print(f"The movie 'Armageddon' correspond to the node {movieToIndex['Armageddon (1998)']}")
print(f"Verify: Actor for node {movieToIndex['Armageddon (1998)']} --> {indexToMovie[movieToIndex['Armageddon (1998)']]}")
search_end_time = time.time()
print(f"SEARCH TIME: {search_end_time-search_start_time}\n")


print("1) MEAN EVALUATION (EXERCISE 1.F) ---------------------------------------------------------------\n")

X = [1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]

for x in X:
    meanYear_start_time = time.time()
    print(f"The Mean up to year {x} is: {averageForYear(x)}")
    meanYear_end_time = time.time()
    print(f"TIME TO EVALUATE MEAN FOR YEAR {x}: {meanYear_end_time - meanYear_start_time}\n")

print(f"Movies without a release date in the dataset are {len(yearsMovie[0])}")

if len(yearsMovie[0]) != 0:
    print(f"First movie found with no release year is: {indexToMovie[next(iter(yearsMovie[0]))]}\n")



print("2) DIAMETER EVALUATION (EXERCISE 2.1) -----------------------------------------------------------\n")

# Not all possible values as been added at X to avoid having too long execution times
X = [1880, 1900, 1920, 1960, 2000, 2020]

# However, it is possible to insert all the decades from 1880 to 2020, with different execution times
# The execution times tend to be of the order of minutes or tens of minutes
# Only the year 2010 is a special case that takes longer to execute

for x in X:
    diameter_start_time = time.time()
    print(f"The Diameter for year {x} is: {diameterUpToYear(x, graphImbd)}")
    diameter_end_time = time.time()
    print(f"DIAMETER EVALUATION FOR YEAR {x} TIME: {diameter_end_time - diameter_start_time}\n")


print("3) ACTOR WHO PARTICIPATED IN MOVIES WITH LARGEST NUMBER OF ACTORS (EXERCISE 3.IV) ---------------\n")

actorPart_start_time = time.time()
print(f"The actor who participated in movies with largest number of actors --> {actorParticipatingFamousMovies(graphImbd)}")
actorPart_end_time = time.time()
print(f"EXECUTION TIME: {actorPart_end_time-actorPart_start_time}\n")

print("4) ACTORS GRAPH AND PAIR OF ACTOR WHO COLLABORATED THE MOST (EXERCISE 4) ----------------------\n")

# It frees up some memory
actorToIndex.clear()
yearsMovie.clear()
yearsActor.clear()
movieToIndex.clear()

actorGraph_start_time = time.time()
actorGraph = createActorGraph(graphImbd)
actorGraph_end_time = time.time()
print("Actor graph is:")
print(actorGraph[0])
print()
print(f"The actors who collaborated the most among themselves are: {indexToActor[actorGraph[1][0]]} and {indexToActor[actorGraph[1][1]]}")
print(f"They collaborated {actorGraph[1][2]} times\n")
print(f"ACTOR GRAPH CONSTRUCTION TIME: {actorGraph_end_time - actorGraph_start_time}\n")
print("Original graph is:")
print(graphImbd)
print()

end_time = time.time()
print("-------END EXECUTION-------")
print(f"TOTAL EXECUTION TIME: {end_time - start_time}")