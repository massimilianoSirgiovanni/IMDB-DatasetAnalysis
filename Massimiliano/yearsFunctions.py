years = {
    0 : [],     # Errors in data
    1870: [],  # (1880, 1890]
    1880: [],   # (1880, 1890]
    1890: [],   # (1890, 1900]
    1900: [],   # (1890, 1910]
    1910: [],   # (1910, 1920]
    1920: [],   # (1920, 1930]
    1930: [],   # (1930, 1940]
    1940: [],   # (1940, 1950]
    1950: [],   # (1950, 1960]
    1960: [],   # (1960, 1970]
    1970: [],   # (1970, 1980]
    1980: [],   # (1980, 1990]
    1990: [],   # (1990, 2000]
    2000: [],   # (2000, 2010]
    2010: [],   # (2010, 2020]
    2020: []    # (2020, 2030]

}

def extractYear(movie):
    for i in range(len(movie)-5, -1, -1):  # Start from the tail of the string because the year is always after the name
        if movie[i] == "(" and (movie[i+1] == '2' or movie[i+1] == '1'): # Checking from the "(" to avoid situation like: (2003/II)
            year = int(movie[i+1] + movie[i+2] + movie[i+3] + movie[i+4])
            if  movie[i+4] == "0":
                return year - 10
            return year - (year % 10)  # Return a string with the decade of the movie
    return 0

def meanForYear(x):

    x, sum, n = meanCheks(x)

    while x > 1870:
        x = x - 10
        n = n + 10
        sum = sum + len(years[x])

    return (sum, n, sum/n)  # NEL PROGETTO FINALE RESTITUIRà SOLO LA MEDIA (Terzo elemento)

def meanCheks(x):
    if type(x) is str:
        x = int(x)
    if x <= 1870:
        return 0, 0, 1

    x = x - (x % 10)

    if x > 2030:
        # DA DISCUTERE COME SCELTA IMPLEMENTATIVA
        n = x - 2030
        x = 2030
        #
        print("ERROR: You can not insert a year over 2030")
        return 0, 0, 1

    return x, 0, 0
