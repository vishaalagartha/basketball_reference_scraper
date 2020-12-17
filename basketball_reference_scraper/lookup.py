import unidecode, os, sys, unicodedata

"""
    Bounded levenshtein algorithm credited to user amirouche on stackoverflow.
    Implementation borrowed from https://stackoverflow.com/questions/59686989/levenshtein-distance-with-bound-limit
"""
def levenshtein(s1, s2, maximum):  
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        if all((x >= maximum for x in distances_)):
            return -1
        distances = distances_
    return distances[-1]

"""
    User input is normalized/anglicized, then assigned a levenshtein score to 
    find the closest matches. If an identical and unique match is found, it is 
    returned. If many matches are found, either identical or distanced, all
    are returned for final user approval.
"""
def lookup(player):
    path = os.path.join(os.path.dirname(__file__), 'br_names.txt')
    normalized = unidecode.unidecode(player)
    matches = []
    
    with open(path) as file:
        Lines = file.readlines()
        for line in Lines:
            """
                A bound of 5 units of levenshtein distance is selected to   
                account for possible misspellings or lingering non-unidecoded 
                characters.
            """
            dist = levenshtein(normalized.lower(), line[:-1].lower(), 5)
            if dist >= 0:
                matches += [(line[:-1], dist)]

    """
        If one match is found, return that one;
        otherwise, return list of likely candidates and allow
        the user to confirm specifiy their selection.
    """
    if len(matches) == 1:
        print("You searched for \"{}\"\n{} result found.\n{}".format(player, len(matches), matches[0][0]))
        print("Results for {}:\n".format(matches[0][0]))
        return matches[0][0]

    elif len(matches) > 1:
        print("You searched for \"{}\"\n{} results found.".format(player, len(matches)))
        matches.sort(key=lambda tup: tup[1])
        i = 0
        for match in matches:
            print("{}: {}".format(i, match[0])) 
            i += 1           
        
        selection = int(input("Pick one: "))
        print("Results for {}:\n".format(matches[selection][0]))
        return matches[selection][0]

    elif len(matches) < 1:
        print("You searched for \"{}\"\n{} results found.".format(player, len(matches)))
        return ""
        
    else:
        print("You searched for \"{}\"\n{} result found.\n{}".format(player, len(matches), matches[0][0]))
        print("Results for {}:\n".format(matches[0][0]))
        return matches[0][0]

    return ""
