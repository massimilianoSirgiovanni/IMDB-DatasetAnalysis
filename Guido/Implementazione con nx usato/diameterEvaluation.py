import networkx as nx
from yearsFunctions import createGraphUpToYear


def diameterUpToYear(x, graph):
    graphYear = createGraphUpToYear(x, graph)
    maxGrade = nodeGradeMax(graphYear)
    diam = diameter(graphYear, maxGrade)
    return diam, graphYear


def nodeGradeMax(graph):
    maxN = -1  # Variable to store the id of the current
    sumMax = 0

    for i in graph.nodes:
        degreeNode = graph.degree(i)
        if degreeNode > sumMax:
            sumMax = degreeNode
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


def Bi(graph, node, lb, level):
    # maxEcc = (0,0)
    '''for i in nodeList:
        temp = eccentricity(graph, i)
        if temp[0] > lb:
            return temp[0]
    return lb'''
    for j in graph.nodes:
        distance = len(nx.shortest_path(graph, node, j))
        if distance == level:
            ecc = nx.eccentricity(graph, j)
            if ecc > lb:
                return ecc
    return lb



def diameter(graph, startNode):
    ecc = nx.eccentricity(graph, startNode)
    i = ecc
    lb = i
    ub = 2 * lb

    while ub > lb:

        bi = Bi(graph, startNode, lb, i)

        if bi > 2 * (i - 1):
            return bi
        else:
            lb = bi
            ub = 2 * (i - 1)
        i = i - 1

    return lb