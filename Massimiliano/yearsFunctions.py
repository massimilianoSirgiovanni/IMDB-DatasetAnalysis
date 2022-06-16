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
    for i in range(0, len(movie)):
        if movie[i] == "(" and (movie[i+1] == '2' or movie[i+1] == '1'):
            return movie[i+1] + movie[i+2] + movie[i+3] + "0"
    return 0

def meanForYear(x):
    return 0