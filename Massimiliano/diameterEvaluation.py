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


def nodeWithMaxDegree(graph, setConsideredNodes):
    # Function that searches for the node with maximum degree

    maxNode = -1  # Variable to store the id of the current node
    maxDegree = 0  # Variable to store the current max degree
    biggestComponent = max(nx.connected_components(graph.subgraph(setConsideredNodes)),
                           key=len)  # It finds the largest connected component

    # For all nodes in biggestComponent connected component we search the node with maximum grade
    for i in biggestComponent:
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

    dSweepDiameter = bfs(graph, startingEcc[1][startingEcc[0]][0], setConsideredNodes)  # calculation of the diameter

    centralNode = floor(dSweepDiameter[0] / 2)  # The midpoint is found

    doubleSweepEcc = eccentricity(graph, dSweepDiameter[2][centralNode], setConsideredNodes)

    if doubleSweepEcc[0] < startingEcc[0]:
        return doubleSweepEcc
    else:
        return startingEcc


def bfs(graph, startNode, setConsideredNodes=0):
    # Bfs algorithm to find the eccentricity of a node
    if setConsideredNodes == 0:
        setConsideredNodes = set(graph.nodes)

    eccPath = {startNode: [startNode]}
    distanceToNodes = {}  # To save all distance of nodes (dictionary of lists)

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
                    if nodeToDistance[nbr] not in distanceToNodes:
                        # Create a list for nodes that have nodeToDistance[nbr] distance
                        distanceToNodes[nodeToDistance[nbr]] = [nbr]
                    else:
                        # the node will be insert in the list of nodes with same distances
                        distanceToNodes[nodeToDistance[nbr]].append(nbr)

                    # Update of maximum distance
                    if nodeToDistance[nbr] > actualMaxDistance:
                        actualMaxDistance = nodeToDistance[nbr]

        index = index + 1  # the nodes become black

    return (actualMaxDistance, distanceToNodes, searchPathAtGivenDistance(eccPath, actualMaxDistance))


def searchPathAtGivenDistance(dictDistances, distance):
    # Select a path with input distance from the dictionary

    for i in dictDistances:
        if len(dictDistances[i]) - 1 == distance:
            return dictDistances[i]

    return 0


def eccentricity(graph, startNode, setConsideredNodes):
    # Calculation of eccentricity

    return bfs(graph, startNode, setConsideredNodes)


def eccBi(graph, nodeList, setConsideredNodes):
    # Maximum eccentricity of nodes in the level i
    maxBi = 0
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
        bi = eccBi(graph, startEcc[1][i], setConsideredNodes)  # max{lb, Bi(u)}
        end_time = time.time()
        print(f"Bi() at {i} level TIME: {end_time - start_time}: with {bi}")

        if max(lb, bi) > 2 * (i - 1):  # Stop condition
            return max(lb, bi)
        else:
            lb = bi
            ub = 2 * (i - 1)
        i = i - 1

    return lb