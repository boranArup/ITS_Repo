from math import sin, asin, cos, sqrt, radians, degrees, pow, atan2
import csv

junctions = [[]]
junctiondists = []

# FUNCTIONS:
# Function to find distances between sets of two coords, given in degrees
def find_dist(x1, y1, x2, y2):
    x1 = radians(x1)
    x2 = radians(x2)
    y1 = radians(y1)
    y2 = radians(y2)
    
    diff_lat = (x1-x2)
    diff_long = (y1-y2)
    a = (sin(diff_lat / 2) * sin(diff_lat / 2) +
            cos(x1) * cos((x2)) *
            sin(diff_long / 2) * sin(diff_long / 2))
    b = atan2(sqrt(a), sqrt(1-a))
    dist_calc = 12742 * b
    return dist_calc



#Prepare Junction data for group ID
filename_junctions = "ManualJunctions.csv"
#Read the existing CSV file and store its content
try:
    junctions_file = open(filename_junctions, mode ='r') 
except OSError:
    print("----------------------------------------------------------------------------------------------------------------------------")
    print("ERROR: Filenames/Location. Please ensure path to junctions file is correct and are enclosed in \"\".")
    print("----------------------------------------------------------------------------------------------------------------------------")
    exit()
    
with junctions_file:
    junctionCSV = csv.reader(junctions_file)
    junctions = list(junctionCSV)
    
for source in range(0, len(junctions)):
    # Determine if in a pair
    junctiondists.append(-1)
    for target in range(0, len(junctions)):
        if junctions[target][2] == junctions[source][2] and junctions[target][1] != junctions[source][1]:
            # These are together
            # Get the distances between matching junctions
            junctiondists[source] = find_dist(float(junctions[source][0]), float(junctions[source][1]), float(junctions[target][0]), float(junctions[target][1]))
            break
    print([source], end=", ")
    print(junctions[source], end=", ")
    print(junctiondists[source])
    
'''
i = 0    
for junction in junctions:
    # Determine if in a pair
    junctiondists.append(-1)
    for pairing in junctions:
        if pairing[2] == junction[2] and pairing[1] != junction[1]:
            # These are together
            # Get the distances between matching junctions
            junctiondists[i] = find_dist(float(junction[0]), float(junction[1]), float(pairing[0]), float(pairing[1]))
            break
   source+= 1
print(junctiondists)'''