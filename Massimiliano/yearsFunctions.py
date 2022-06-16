years = {

    '1890': [],
    '1900': [],
    '1910': [],
    '1920': [],
    '1930': [],
    '1940': [],
    '1950': [],
    '1960': [],
    '1970': [],
    '1980': [],
    '1990': [],
    '2000': [],
    '2010': [],
    '2020': []

}

def extractYear(movie):
    for i in range(len(movie)-5, -1, -1):  # Start from the tail of the string because the year is always after the name
        if movie[i] == "(" and (movie[i+1] == '2' or movie[i+1] == '1'): # Checking from the "(" to avoid situation like: (2003/II)
            return movie[i+1] + movie[i+2] + movie[i+3] + "0"  # Return a string with the decade of the movie
    return 0

def meanForYear(x):
    return 0