import networkx as nx
import time
from yearsFunctions import *
from diameterEvaluation import *
from actorsOperations import *
from graphConstruction import *

start_time = time.time()
graph1 = createGraph("prova2.tsv")
#graph = createGraph("imdb-actors-actresses-movies.tsv")
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")
print(graph1)
x = 2000
print(f"The Mean up to year {x} is: {meanForYear(x)}")
print(years[0])

if len(years[0]) != 0:
    for i in years[0]:
        print(indexToMovie[i])
        break

start_time = time.time()
print(f"Esercizio 3.IV: {actorParticFamousMovies(graph1)}")
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")
'''print(indexToMovie[1967])
print(indexToMovie[18966])
print(indexToMovie[53495])
print(indexToMovie[93776])
print(indexToMovie[123315])'''

x = 2020
start_time = time.time()
diameter = diameterUpToYear(x, graph1)
print(f"The Diameter is: {diameter}")
end_time = time.time()
print(f"EXECUTION TIME: {end_time-start_time}")

actorToIndex.clear()
years.clear()
yearsActor.clear()
movieToIndex.clear()


start_time = time.time()
graph3 = createActorGraph(graph1)
end_time = time.time()
print(graph3[0])
print(f"Gli attori che hanno collaborato maggiormente sono: {indexToActor[graph3[1][0]]} e {indexToActor[graph3[1][1]]}")
print(f"Hanno collaborato {graph3[1][2]} volte")

print(f"EXECUTION TIME: {end_time - start_time}")

print(graph1)



