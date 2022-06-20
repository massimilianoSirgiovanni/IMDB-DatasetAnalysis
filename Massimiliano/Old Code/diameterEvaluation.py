import networkx as nx
from yearsFunctions import createGraphUpToYear


def diameterUpToYear(x, graph):
    graphYear = createGraphUpToYear(x, graph)
    maxGrade = nodeGradeMax(graphYear)
    diam = diameter(graphYear, maxGrade)
    return diam


def nodeGradeMax(graph):
    maxN = -1  # Variable to store the id of the current
    sumMax = 0

    for i in graph.nodes:
        neighbors = list(graph.neighbors(i))
        sumN = len(neighbors)
        if sumN > sumMax:
            sumMax = sumN
            maxN = i
    if maxN == -1:
        print("ERROR: NO NODE FOUND IN THE GRAPH")
        return -1
    else:
        return maxN


def bfs(graph, startNode):
    dizionarioEsterno = {}

    nodeDistance = {startNode: 0}

    nodeToVisit = [startNode]
    index = 0
    max = 0

    while index < len(nodeToVisit):
        currentVert = nodeToVisit[index]
        neighbors = list(graph.neighbors(currentVert))

        for nbr in neighbors:
            if nbr not in nodeDistance:
                nodeToVisit.append(nbr)
                nodeDistance[nbr] = nodeDistance[currentVert] + 1
                if nodeDistance[nbr] not in dizionarioEsterno:
                    dizionarioEsterno[nodeDistance[nbr]] = [nbr]
                else:
                    dizionarioEsterno[nodeDistance[nbr]].append(nbr)

                if nodeDistance[nbr] > max:
                    max = nodeDistance[nbr]
        index = index + 1

    return (max, dizionarioEsterno)


# Calcolo dell'eccentricità
def eccentricity(graph, startNode):
    max = bfs(graph, startNode)

    return max


def Bi(graph, nodeList, lb):
    # maxEcc = (0,0)
    for i in nodeList:
        temp = eccentricity(graph, i)

        if temp[0] > lb:
            return temp[0]

    return lb


def diameter(graph, startNode):
    bfsTuple = eccentricity(graph, startNode)
    i = bfsTuple[0]
    lb = i
    ub = 2 * lb

    while ub > lb:

        bi = Bi(graph, bfsTuple[1][i], lb)

        if bi > 2 * (i - 1):
            return bi
        else:
            lb = bi
            ub = 2 * (i - 1)
        i = i - 1

    return lb


