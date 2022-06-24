# Dictionary for movies
yearsMovie = {
    0: set(),  # Errors in data
    1870: set(),  # (1870, 1880]
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
    1870: set(),  # (1870, 1880]
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


def extractYear(movie):
    # Function for extracting the year from each line of the file

    for i in range(len(movie) - 6, -1,
                   -1):  # Start from the tail of the string because the year is always after the name

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

    x, yearSum, n = meanChecks(x)  # Preliminary checks

    # Calculation of the components for the average
    while x > 1870:
        x = x - 10
        n = n + 10
        yearSum = yearSum + len(yearsMovie[x])

    return yearSum / n  # Calculation of the average


def meanChecks(x):
    # Preliminary checks for the selected year x.
    # It must be a value between 1870 and 2030

    if type(x) is str:
        x = int(x)

    if x <= 1870:
        return 0, 0, 1

    if (x % 10) != 0:
        tmp = x
        x = x - (x % 10)  # Calculation of the year's decade
        print(f"ATTENTION: The year {tmp} is not a decade so it was transformed to {x}")

    if x >= 2030:
        print("ERROR: You can not insert a year over 2020")
        return 0, 0, 1

    return x, 0, 0


# Function useful for Exercise 2.1
def createSetUpToYear(x):
    # Creation of a common set that contains movies and actors up to the year x

    x = meanChecks(x)[0]  # Preliminary checks
    unionSet = set()  # Creation of the set

    while x > 1870:  # Initialization of the set
        x = x - 10
        unionSet = unionSet.union(yearsMovie[x])
        unionSet = unionSet.union(yearsActor[x])

    return unionSet