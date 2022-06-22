import networkx as nx
from yearsFunctions import createGraphUpToYear
import time


def diameterUpToYear(x, graph):
    setYear = createGraphUpToYear(x, graph)
    if len(setYear) == 0:
        print(f"ERROR: There are no movies up to the year {x}")
        return 0
    maxGrade = nodeGradeMax(graph, setYear)
    diam = diameter(graph, maxGrade)
    return diam


def nodeGradeMax(graph, set):
    maxN = -1  # Variable to store the id of the current
    sumMax = 0
    
    
    giant = max(nx.connected_components(graph.subgraph(set)), key=len)
    
    for i in giant:
        degreeNode = graph.degree(i)
        if degreeNode > sumMax:
            sumMax = degreeNode
            maxN = i
    if maxN == -1:
        print("ERROR: NO NODE FOUND IN THE GRAPH")
        return -1
    else:
        return maxN


def bfs(graph, startNode, setNode):
    dizionarioEsterno = {}

    nodeDistance = {startNode: 0}

    nodeToVisit = [startNode]
    index = 0
    max = 0

    while index < len(nodeToVisit):
        currentVert = nodeToVisit[index]
        neighbors = list(graph.neighbors(currentVert))

        for nbr in neighbors:
            if nbr in setNode:
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
def eccentricity(graph, startNode, set):
    max = bfs(graph, startNode, set)

    return max


#def Bi(graph, node, lb, level):
def Bi(graph, nodeList, lb, set):
    # maxEcc = (0,0)
    for i in nodeList:
        temp = eccentricity(graph, i, set)

        #if temp[0] >= lb:
        if temp[0] >= lb:#######era > e hai aggiunto =   if temp[0] >= lb:#######era > e hai aggiunto =
            return temp[0]

    return lb
    '''for j in graph.nodes:
        distance = len(nx.shortest_path(graph, node, j))-1
        if distance == level:
            ecc = nx.eccentricity(graph, j)
            if ecc > lb:
                return ecc
    return lb'''



'''def diameter(graph, startNode):
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
    return lb'''

def diameter(graph, startNode, setNode):
    start_time = time.time()
    bfsTuple = eccentricity(graph, startNode, setNode)
    end_time = time.time()
    print(f"Compute bfsTuple TIME: {end_time - start_time}")
    i = bfsTuple[0]
    lb = i
    ub = 2 * lb

    while ub > lb:
        start_time = time.time()
        bi = Bi(graph, bfsTuple[1][i], lb, setNode)
        end_time = time.time()
        print(f"Bi() at {i} level TIME: {end_time - start_time}")


        if bi > 2 * (i - 1):
            return bi
        else:
            lb = bi
            ub = 2 * (i - 1)
        i = i - 1

    return lb