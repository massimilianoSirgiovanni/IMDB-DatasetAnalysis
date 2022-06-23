import networkx as nx
from yearsFunctions import createSetUpToYear
import time
from math import ceil


# Diameter up to the selected year x
def diameterUpToYear(x, graph):

    start_time = time.time()
    commonSetYear = createSetUpToYear(x) # Common set for movies and actors
    end_time = time.time()
    print(f"EXECUTION TIME: {end_time - start_time}")
    
    # We find the node with maximum grade in the biggest connected component
    start_time = time.time()
    if len(commonSetYear) == 0:
        print(f"ERROR: There are no movies up to the year {x}")
        return 0
    maxGrade = nodeWithMaxDegree(graph, commonSetYear)
    end_time = time.time()
    print(f"EXECUTION TIME: {end_time - start_time}")
    
    # We use the 2-Sweep algorithm starting from the node with max grade
    start_time = time.time()
    startNode = doubleSweep(graph, maxGrade, commonSetYear)
    end_time = time.time()
    print(f"EXECUTION TIME: {end_time - start_time}")
    
    # Diameter evaluation
    diam = diameter(graph, startNode, commonSetYear)
    return diam


# Function that searches for the node with maximum degree
def nodeWithMaxDegree(graph, set):
    
    maxNode = -1  # Variable to store the id of the current node
    maxDegree = 0 # Variable to store the current max degree
    biggestComponent = max(nx.connected_components(graph.subgraph(set)), key=len) # It finds the largest connected component
    
    
    # For all nodes in the biggestComponent connected component we search the node with maximum grade
    for i in biggestComponent:
        degreeNode = graph.degree(i)
        
        if degreeNode > maxDegree: # Update of the node of maximum degree
            maxDegree = degreeNode
            maxNode = i
            
    if maxNode == -1: # Empty graph case
        print("ERROR: NO NODE FOUND IN THE GRAPH")
        return -1
    
    else:
        return maxNode # Node with maximum degree


# 2-Sweep procedure
def doubleSweep(graph, startNode, set):
    
    startingEcc = bfs(graph, startNode, set) # Eccentricity of the starting node
    dSweepDiameter = bfs(graph, startingEcc[1][startingEcc[0]][0], set) # calculation of the 2-Sweep diameter
    print(dSweepDiameter[0])
    centralNode = ceil(dSweepDiameter[0]/2) # The midpoint is found
    print(dSweepDiameter[2])
    print(dSweepDiameter[2][centralNode])
    return dSweepDiameter[2][centralNode]



# Bfs algorithm to find the eccentricity of a node
def bfs(graph, startNode, setCCNode):
    
    eccPath = {startNode: [startNode]}
    distancesToNodes = {} # To save all distance of nodes (dictionary of lists)

    nodeDistance = {startNode: 0} # To update distance of nodes

    nodeToVisit = [startNode]
    index = 0
    actualMaxDistance = 0

    # Until we have visited all the nodes
    while index < len(nodeToVisit):
        currentVert = nodeToVisit[index]
        neighbors = list(graph.neighbors(currentVert))


        for nbr in neighbors: # the nodes become gray
            
            if nbr in setCCNode: # if the each node is in the selected connected component
                if nbr not in nodeDistance: # if the node is white
                
                    # In this case we add nbr to the nodes path
                    eccPath[nbr] = eccPath[currentVert].copy()
                    eccPath[nbr].append(nbr)
                    nodeToVisit.append(nbr)
                    nodeDistance[nbr] = nodeDistance[currentVert] + 1 # Update of the distance
                    
                    # Update of distances between nodes
                    if nodeDistance[nbr] not in distancesToNodes:
                        distancesToNodes[nodeDistance[nbr]] = [nbr] # Create a list for nodes that have the same distance
                    else:
                        distancesToNodes[nodeDistance[nbr]].append(nbr) # the node will be insert in the list of nodes with same distances
                    
                    # Update of maximum distance
                    if nodeDistance[nbr] > actualMaxDistance:
                        actualMaxDistance = nodeDistance[nbr]
        index = index + 1
        
    # Select the node with max distance that the algorithm found
    for i in eccPath:
        if len(eccPath[i]) - 1 == actualMaxDistance:
            return (actualMaxDistance, distancesToNodes, eccPath[i])
    return 0




# Calculation of eccentricity
def eccentricity(graph, startNode, set):
    max = bfs(graph, startNode, set)

    return max


# Maximum eccentricity of nodes in the level i
def eccBi(graph, nodeList, lb, set):
    
    for i in nodeList:
        actualBiDistance = eccentricity(graph, i, set)
        
        # Selection of max{lb, Bi(u)}
        if actualBiDistance[0] > lb:
            return actualBiDistance[0]

    return lb


# Diameter of a connected component
def diameter(graph, startNode, setCCNode):
    start_time = time.time()
    bfsTuple = eccentricity(graph, startNode, setCCNode)
    end_time = time.time()
    print(f"Compute bfsTuple TIME: {end_time - start_time}")
    
    i = bfsTuple[0]
    lb = i
    ub = 2 * lb

    while ub > lb:
        start_time = time.time()
        bi = eccBi(graph, bfsTuple[1][i], lb, setCCNode) # max{lb, Bi(u)}
        end_time = time.time()
        print(f"Bi() at {i} level TIME: {end_time - start_time}: with {bi}")


        if bi > 2 * (i - 1): # Stop condition
            return bi
        else:
            lb = bi
            ub = 2 * (i - 1)
        i = i - 1

    return lb


