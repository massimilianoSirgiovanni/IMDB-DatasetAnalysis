import networkx as nx
from yearsFunctions import createSetUpToYear
import time
from math import floor


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

    startingEcc = bfs(graph, startNode, setConsideredNodes)  # Eccentricity of the starting node

    dSweepDiameter = bfs(graph, startingEcc[1][startingEcc[0]][0], setConsideredNodes, pathsReturn=1)  # calculation of the diameter

    return combinedChoice(dSweepDiameter, startingEcc, graph, setConsideredNodes)

def combinedChoice(dSweepDiameter, gradeMaxEcc, graph, setConsideredNodes):
    # Method linked to the doubleSweep() function
    centralNode = floor(dSweepDiameter[0] / 2)  # The midpoint is found
    minEcc = gradeMaxEcc
    lefts = len(dSweepDiameter[2])
    for i in dSweepDiameter[2]:
        lefts = lefts - 1
        doubleSweepEcc = eccentricity(graph, i[centralNode], setConsideredNodes)
        if minEcc[0] > doubleSweepEcc[0] or (minEcc[0] == doubleSweepEcc[0] and len(doubleSweepEcc[1][doubleSweepEcc[0]]) < len(minEcc[1][minEcc[0]])):
            minEcc = doubleSweepEcc
        if lefts > len(minEcc[1][minEcc[0]]):
            return minEcc

    return minEcc


def bfs(graph, startNode, setConsideredNodes=0, pathsReturn=0):
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
                    eccPath[nbr] = eccPath[currentVert].copy()
                    eccPath[nbr].append(nbr)
                    nodeToVisit.append(nbr)    # the nodes become gray
                    nodeToDistance[nbr] = nodeToDistance[currentVert] + 1

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

    return bfs(graph, startNode, setConsideredNodes)


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
        lb = max(lb, bi)

        if lb > 2 * (i - 1):  # Stop condition
            return lb

        ub = 2 * (i - 1)
        i = i - 1

    return lb