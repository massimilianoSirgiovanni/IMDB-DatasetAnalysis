# A RAM of 16GB or higher is recommended for running

import random
from yearsFunctions import *
from diameterEvaluation import *
from actorsOperations import *
from graphConstruction import *

print("-------START EXECUTION-------\n")
print("0) GRAPH CONSTRUCTION --------------------------------------------------------------------------\n")
start_time = time.time()
#graphImbd = createGraph("prova2.tsv")
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

X = [1900, 1920, 1950, 1990, 2020]

for x in X:
    meanYear_start_time = time.time()
    print(f"The Mean up to year {x} is: {averageForYear(x)}")
    meanYear_end_time = time.time()
    print(f"TIME TO EVALUATE MEAN FOR YEAR {x}: {meanYear_end_time - meanYear_start_time}\n")

print(f"Movies without a release date in the dataset are {len(yearsMovie[0])}")

if len(yearsMovie[0]) != 0:
    print(f"First movie found with no release year is: {indexToMovie[next(iter(yearsMovie[0]))]}\n")

print("2) DIAMETER EVALUATION (EXERCISE 2.1) -----------------------------------------------------------\n")

X = [2000]

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




