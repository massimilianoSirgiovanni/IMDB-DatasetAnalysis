import networkx as nx
from yearsFunctions import createSetUpToYear
import time
from math import ceil


def diameterUpToYear(x, graph):
# Diameter up to the selected year x
    
    setConsideredNodes = createSetUpToYear(x) # Common set for movies and actors
    
    # Find the node with maximum grade in the biggest connected component
    if len(setConsideredNodes) == 0:
        print(f"ERROR: There are no movies up to the year {x}")
        return 0
    maxGrade = nodeWithMaxDegree(graph, setConsideredNodes)
    
    # Use the 2-Sweep algorithm starting from the node with max grade
    startNode = doubleSweep(graph, maxGrade, setConsideredNodes)
    
    # Diameter evaluation
    diam = diameter(graph, startNode, setConsideredNodes)
    return diam



def nodeWithMaxDegree(graph, setConsideredNodes):
# Function that searches for the node with maximum degree
    
    maxNode = -1  # Variable to store the id of the current node
    maxDegree = 0 # Variable to store the current max degree
    biggestComponent = max(nx.connected_components(graph.subgraph(setConsideredNodes)), key=len) # It finds the largest connected component
    
    
    # For all nodes in biggestComponent connected component we search the node with maximum grade
    for i in biggestComponent:
        degreeNode = graph.degree(i) # the degree() function is from NetworkX
        
        if degreeNode > maxDegree: # Update of the node of maximum degree
            maxDegree = degreeNode
            maxNode = i
            
    if maxNode == -1: # Empty graph case
        print("ERROR: NO NODE FOUND IN THE GRAPH")
        return -1
    
    else:
        return maxNode # Node with maximum degree


def doubleSweep(graph, startNode, setConsideredNodes):
# 2-Sweep procedure
    
    startingEcc = bfs(graph, startNode, setConsideredNodes) # Eccentricity of the starting node
    
    dSweepDiameter = bfs(graph, startingEcc[1][startingEcc[0]][0], setConsideredNodes) # calculation of the 2-Sweep diameter
    
    centralNode = ceil(dSweepDiameter[0]/2) # The midpoint is found
    
    return dSweepDiameter[2][centralNode]



def bfs(graph, startNode, setConsideredNodes):
# Bfs algorithm to find the eccentricity of a node
    
    eccPath = {startNode: [startNode]}
    distanceToNodes = {} # To save all distance of nodes (dictionary of lists)

    nodeToDistance = {startNode: 0} # To memorize distance of nodes

    nodeToVisit = [startNode]
    index = 0
    actualMaxDistance = 0

    # Until we have visited all the nodes
    while index < len(nodeToVisit):
        currentVert = nodeToVisit[index]
        neighbors = list(graph.neighbors(currentVert))


        for nbr in neighbors:
            
            if nbr in setConsideredNodes: # if nbr had the property of the set
                if nbr not in nodeToDistance: # if the node is white
                
                    # In this case we add nbr to the nodes path
                    eccPath[nbr] = eccPath[currentVert].copy()
                    eccPath[nbr].append(nbr)
                    nodeToVisit.append(nbr)
                    nodeToDistance[nbr] = nodeToDistance[currentVert] + 1 # the nodes become gray
                    
                    # Add nbr to distanceToNodes
                    if nodeToDistance[nbr] not in distanceToNodes:
                        distanceToNodes[nodeToDistance[nbr]] = [nbr] # Create a list for nodes that have nodeToDistance[nbr] distance
                    else:
                        distanceToNodes[nodeToDistance[nbr]].append(nbr) # the node will be insert in the list of nodes with same distances
                    
                    # Update of maximum distance
                    if nodeToDistance[nbr] > actualMaxDistance:
                        actualMaxDistance = nodeToDistance[nbr]
                        
        index = index + 1 # the nodes become black
    
    return (actualMaxDistance, distanceToNodes, searchPathAtGivenDistance(eccPath, actualMaxDistance))


def searchPathAtGivenDistance(dictDistances, distance):
# Select a path with input distance from the dictionary

    for i in dictDistances:
        if len(dictDistances[i]) - 1 == distance:
            return dictDistances[i]
        
    return 0
    


def eccentricity(graph, startNode, setConsideredNodes):
# Calculation of eccentricity

    max = bfs(graph, startNode, setConsideredNodes)

    return max


def eccBi(graph, nodeList, lb, setConsideredNodes):
# Maximum eccentricity of nodes in the level i
    
    for i in nodeList:
        actualBiDistance = eccentricity(graph, i, setConsideredNodes)
        
        # Selection of max{lb, Bi(u)}
        if actualBiDistance[0] > lb:
            return actualBiDistance[0]

    return lb



def diameter(graph, startNode, setConsideredNodes):
# Diameter of a connected component
    
    start_time = time.time()
    bfsTuple = eccentricity(graph, startNode, setConsideredNodes)
    # bfsTuple = (eccentricity, distance dictionary, path with length equal to eccentricity)
    end_time = time.time()
    print(f"Compute bfsTuple TIME: {end_time - start_time}")
    
    i = bfsTuple[0] # eccentricity of starting node
    lb = i
    ub = 2 * lb

    while ub > lb:
        start_time = time.time()
        bi = eccBi(graph, bfsTuple[1][i], lb, setConsideredNodes) # max{lb, Bi(u)}
        end_time = time.time()
        print(f"Bi() at {i} level TIME: {end_time - start_time}: with {bi}")


        if bi > 2 * (i - 1): # Stop condition
            return bi
        else:
            lb = bi
            ub = 2 * (i - 1)
        i = i - 1

    return lb


