# Personal paths for use
# Code is ran with variation of this in terminal:
# C:\Users\leonardo.boran\OneDrive - Arup\ITS_Repo>C:/Users/leonardo.boran/AppData/Local/miniforge3/envs/arup-env/python.exe "c:/Users/leonardo.boran/OneDrive - Arup/ITS_Repo/AutomatedGrouping_Expansion.py" TestCoordsCSV.csv OutputCSV.csv
#               ^                                                                            ^                                                               ^               ^
#               |                                                                            |                                                               |               |
#              can be replaced by just "python" outlines environment                        The path of this python file                                           Name and path of input and output files separated
#                                                                                                                                                           Note: include quotes where there are spaces.

from sys import argv
from math import sin, cos, sqrt, radians, degrees, atan2
import csv
import bisect

# Define the setpoint for maximum distance considered as a grouping of equipments between two objects
# Note: As long as a node is close enough to any of the nodes/equipment in a group it joins the group even if distance
# to some nodes is larger than setpoint!
MAX_GROUP_DIST = 0.035
data = [[]]

junctions = [
    {"Lat":53.319129, "Long":-6.364785, "Junction":"01", "Number Junctions":2},
    {"Lat":53.317002, "Long":-6.374231, "Junction":"01", "Number Junctions":2},
    {"Lat":53.314538, "Long":-6.38374, "Junction":"1A", "Number Junctions":2},
    {"Lat":53.311893, "Long":-6.397661, "Junction":"1A", "Number Junctions":2},
    {"Lat":53.304472, "Long":-6.412533, "Junction":"2", "Number Junctions":2},
    {"Lat":53.299882, "Long":-6.422897, "Junction":"2", "Number Junctions":2},
    {"Lat":53.294148, "Long":-6.428512, "Junction":"3", "Number Junctions":2},
    {"Lat":53.293394, "Long":-6.430316, "Junction":"3", "Number Junctions":2},
    {"Lat":53.29171, "Long":-6.436477, "Junction":"3A", "Number Junctions":2},
    {"Lat":53.291735, "Long":-6.438328, "Junction":"3A", "Number Junctions":2},
    {"Lat":53.286277, "Long":-6.453426, "Junction":"4", "Number Junctions":2},
    {"Lat":53.282344, "Long":-6.473934, "Junction":"4", "Number Junctions":2},
    {"Lat":53.268384, "Long":-6.521651, "Junction":"5", "Number Junctions":2},
    {"Lat":53.268361, "Long":-6.521136, "Junction":"5", "Number Junctions":2},
    {"Lat":53.259159, "Long":-6.54885, "Junction":"6", "Number Junctions":2},
    {"Lat":53.257866, "Long":-6.552666, "Junction":"6", "Number Junctions":2},
    {"Lat":53.254697, "Long":-6.565342, "Junction":"7", "Number Junctions":2},
    {"Lat":53.252001, "Long":-6.580663, "Junction":"7", "Number Junctions":2},
    {"Lat":53.2432, "Long":-6.608322, "Junction":"8", "Number Junctions":2},
    {"Lat":53.239547, "Long":-6.61786, "Junction":"8", "Number Junctions":2},
    {"Lat":53.235729, "Long":-6.627183, "Junction":"9", "Number Junctions":2},
    {"Lat":53.236506, "Long":-6.640046, "Junction":"9", "Number Junctions":2},
    {"Lat":53.236928, "Long":-6.677033, "Junction":"9A", "Number Junctions":2},
    {"Lat":53.23096, "Long":-6.690526, "Junction":"9A", "Number Junctions":2},
    {"Lat":53.21081, "Long":-6.708256, "Junction":"10", "Number Junctions":2},
    {"Lat":53.204215, "Long":-6.718432, "Junction":"10", "Number Junctions":2},
    {"Lat":53.174512, "Long":-6.746361, "Junction":"11", "Number Junctions":1},
    {"Lat":53.1626, "Long":-6.817389, "Junction":"12", "Number Junctions":2},
    {"Lat":53.161878, "Long":-6.828102, "Junction":"12", "Number Junctions":2},
    {"Lat":53.151289, "Long":-6.910512, "Junction":"13", "Number Junctions":2},
    {"Lat":53.15311, "Long":-6.926945, "Junction":"13", "Number Junctions":2},
    {"Lat":53.147085, "Long":-7.007526, "Junction":"14", "Number Junctions":2},
    {"Lat":53.144047, "Long":-7.022556, "Junction":"14", "Number Junctions":2},
    {"Lat":53.091381, "Long":-7.168647, "Junction":"15", "Number Junctions":2},
    {"Lat":53.086276, "Long":-7.177975, "Junction":"15", "Number Junctions":2},
    {"Lat":53.054243, "Long":-7.234712, "Junction":"16", "Number Junctions":2},
    {"Lat":53.046533, "Long":-7.242269, "Junction":"16", "Number Junctions":2},
    {"Lat":53.013368, "Long":-7.294671, "Junction":"17", "Number Junctions":2},
    {"Lat":53.013661, "Long":-7.311163, "Junction":"17", "Number Junctions":2},
    {"Lat":53.019935, "Long":-7.33462, "Junction":"18", "Number Junctions":2},
    {"Lat":53.018383, "Long":-7.350444, "Junction":"18", "Number Junctions":2},
    {"Lat":52.924782, "Long":-7.477539, "Junction":"19", "Number Junctions":1},
    {"Lat":52.924048, "Long":-7.622757, "Junction":"21", "Number Junctions":2},
    {"Lat":52.92307, "Long":-7.637203, "Junction":"21", "Number Junctions":2},
    {"Lat":52.922166, "Long":-7.792741, "Junction":"22", "Number Junctions":2},
    {"Lat":52.92113, "Long":-7.795943, "Junction":"22", "Number Junctions":2},
    {"Lat":52.886449, "Long":-7.943307, "Junction":"23", "Number Junctions":2},
    {"Lat":52.886265, "Long":-7.946158, "Junction":"23", "Number Junctions":2},
    {"Lat":52.860843, "Long":-8.114353, "Junction":"24", "Number Junctions":2},
    {"Lat":52.858749, "Long":-8.125175, "Junction":"24", "Number Junctions":2},
    {"Lat":52.851924, "Long":-8.149167, "Junction":"25", "Number Junctions":2},
    {"Lat":52.848736, "Long":-8.167271, "Junction":"25", "Number Junctions":2},
    {"Lat":52.84482, "Long":-8.240377, "Junction":"26", "Number Junctions":2},
    {"Lat":52.84499, "Long":-8.258259, "Junction":"26", "Number Junctions":2},
    {"Lat":52.758912, "Long":-8.403565, "Junction":"27", "Number Junctions":2},
    {"Lat":52.754809, "Long":-8.414376, "Junction":"27", "Number Junctions":2},
    {"Lat":52.678343, "Long":-8.511562, "Junction":"28", "Number Junctions":2},
    {"Lat":52.669863, "Long":-8.515563, "Junction":"28", "Number Junctions":2},
    {"Lat":52.65039, "Long":-8.558517, "Junction":"29", "Number Junctions":2},
    {"Lat":52.644305, "Long":-8.567894, "Junction":"29", "Number Junctions":2},
    {"Lat":52.640676, "Long":-8.615899, "Junction":"30", "Number Junctions":1}
    ]
junctiondists = []
markers = [[]]
dir = ["Direction"]

# Location should relate to path of python file like input and output arguments
filename_junctions = 'All_M7_Junctions.csv' # "All_M7_Junctions.csv"

# FUNCTIONS:
# Function to find angle between junctions (3 coords)
def find_angle(x1,y1,x2,y2,x3,y3):
# Calculate the vectors between the points
    ang = degrees(atan2(y3-y2, x3-x2) - atan2(y1-y2, x1-x2))
    if ang < 0:
        ang = ang * -1
    if ang > 180:
        ang = 360 - ang
    return ang


# Checks if junctions are in the same direction
def same_dir(j1, j2, j3):
    ########################################################################################################
    # Edit acute angle (degrees if motorway or road has large bends or small distances between junctions)  #
    ########################################################################################################
    acute = 80
    
    angle = find_angle(float(j1["Lat"]),float(j1["Long"]),float(j2["Lat"]),float(j2["Long"]),float(j3["Lat"]),float(j3["Long"]))
    if angle > acute:
        return True
    else:
        return False


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


#M7E-J9J9A-22141E   (-AID)
# Prepare ID string
def form_groupID(idx):
    print()
    print()
    id = ""
    
    # Match to marker allong motorway
    # Road name
    
    # Save 3 closest markers as this ensures you get the nearest and the next closest one to the pair of two
    # which indicates what side of the "gate we are on"
    markeridx = [0,0,0]
    # Markers are 500m appart so conservative 0.75km max set as any point on the road has to be in range of 3-6 markers
    # but these margins are slightly expanded to allow for equipment to be slightly offroad
    markerdist = [0.75,0.75,0.75]
    for i in range(0,len(markers)):
        dist = find_dist(float(markers[i][1]),float(markers[i][0]),f_lat[idx],f_long[idx])
        if markerdist[0] > dist:
            markerdist[0] = dist
            markeridx[0] = i
        elif markerdist[1] > dist:
            markerdist[1] = dist
            markeridx[1] = i
        elif markerdist[2] > dist:
            markerdist[2] = dist
            markeridx[2] = i
            
    # Markersidx shows nearest marker
    # Eg. M7E_
    used_dir = ""
    
    # Trust the information most from the equipment list
    # Is this information not available
    if dir[idx] == "":
        used_dir = markers[markeridx[0]][6]
    else:
        if markers[markeridx[0]][6] == dir[idx]:
            used_dir = markers[markeridx[0]][6]
        else:
            used_dir = dir[idx]
    id = markers[markeridx[0]][4] + markers[markeridx[0]][5] + used_dir + "-"
    
    # Match to 2 nearest junctions
    max_between_junct = 100
    
    minjuncts = []
    for i in range(0,len(junctions)):
        dist = find_dist(float(junctions[i]["Lat"]),float(junctions[i]["Long"]),f_lat[idx],f_long[idx])
        if dist > max_between_junct:
            i = -1
            dist = max_between_junct
        bisect.insort(minjuncts, [dist, i])
            
    # Junctions
    #print("Near id "+ str(minjuncts[0][1]), end=" ")
    if minjuncts[0][1] == -1 or markerdist[0] >= 0.75:
        # There is no near junction
        id = "NOT-IN-SCOPE"
        print(f_lat[idx], end=" ")
        print(f_long[idx], end="  ")
        print(id, end="  ")
        print(minjuncts[0][0])
        
        return(id) 
    
    else:
        # Calculate if between junction pair
        dist0 = find_dist(float(junctions[minjuncts[0][1]]["Lat"]),float(junctions[minjuncts[0][1]]["Long"]),f_lat[idx],f_long[idx])
        dist1 = find_dist(float(junctions[minjuncts[1][1]]["Lat"]),float(junctions[minjuncts[1][1]]["Long"]),f_lat[idx],f_long[idx])
        
        # Default to using 0 and 1 as normal
        chosen_idx = minjuncts[1][1]
        
        # Check if 0 and 1 are *NOT* two ends of a junction and the equipment is within these bounds
        print(junctions[minjuncts[0][1]], end=" ")
        #print(", Distance between junctions: ", end=" ")
        #print(junctiondists[minjuncts[0][1]], end=" ")
        
        #TODO: Put a Title on the on the manual junctions csv for clarity and then adjust the code accordingly
        #TODO: Find out if the closest junction is part of a pair or not and sequentially 
        # chose which method to use when calculating the two "Between" junctions
        
        print()
        # Is this near a single junction, needed as causes problems with current algorithm
        if int(junctions[minjuncts[0][1]]["Number Junctions"]) == 1:
            # Initialise 3 current junctions: Equipment location, nearest junction and next nearest
            # If the nearest and the next nearest are in the same direction then the equipment is not located between the two
            points = [{"Lat":f_lat[idx],"Long":f_long[idx]}, junctions[minjuncts[0][1]], junctions[minjuncts[1][1]]]
        #############################################################################################################
            print("------------This nearest junction only has one neighbor-------------")
            junction_idx = 1 # index of correct closest junction
            #print(points)
            while same_dir(points[junction_idx - 1], points[junction_idx], points[junction_idx + 1]):
                # Shift the junctions down by appending to the front and then popping off the last one
                print(minjuncts[junction_idx][1])
                junction_idx += 1
                points.append(junctions[minjuncts[junction_idx][1]])
            
            #Correct index to use has been set
            chosen_idx = minjuncts[junction_idx][1]
        #############################################################################################################


        # Only near a junction pair
        else:
            if junctiondists[minjuncts[0][1]] < dist0 or junctiondists[minjuncts[0][1]] < dist1:
        
                #print("Not within junction")        
                # Check if 0 and 1 have same junction name
                if junctions[minjuncts[0][1]]["Junction"] == junctions[minjuncts[1][1]]["Junction"]:
                    #print("Has the same name tho")
                    
                    # Check if 2 is a suitable junction or is the following junction nearer by and being incorrectly chosen
                    i = 0
                    
                    while same_dir(junctions[minjuncts[i][1]],junctions[minjuncts[i+1][1]],junctions[minjuncts[i+2][1]]):
                        # Go to the next junction and recheck if its in the same direction
                        i += 1
                
                    # Not in the same direction as the two junction parts use this
                    chosen_idx = minjuncts[i+2][1]   
            else:
                #print("Within Junction")
                pass
                
        id = id + "J" + junctions[minjuncts[0][1]]["Junction"].zfill(2) + "J" + junctions[chosen_idx]["Junction"].zfill(2)

    distuse = 0.0
    lenghtofroad = 0.0
    # Make sure not to select the maker from the same gate
    # If 1 index is not the same as the 0 gate use this
    if float(markers[markeridx[0]][2]) != float(markers[markeridx[1]][2]):
        distuse = float(markers[markeridx[1]][2])
    # Use marker at index 2 as the different one
    else:
         distuse = float(markers[markeridx[2]][2])
         
    if distuse - float(markers[markeridx[0]][2]) < 0:
        lenghtofroad = round((float(markers[markeridx[0]][2]) - markerdist[0]) * 1000)
    else:
        lenghtofroad = round((float(markers[markeridx[0]][2]) + markerdist[0]) * 1000)

    # Eg. M7E_J9J9A_22141E
    id = id + "-"
    id = id + str(lenghtofroad).zfill(5) + used_dir
    
    if "JEND" in id or "JSTART" in id:
        id = "NOT-IN-SCOPE"
        
    print(f_lat[idx], end=" ")
    print(f_long[idx])
    print(id, end="  ")
    #print(minjuncts[0][0])
    
    return(id)

# Start of "main"
# Warn about possible issue relating to ability to open correctly listed files:
print()   
print("----------------------------------------------------------------------------------------------------------------------------")
print("NOTE: If the following error occurs, please make sure either the write file is not currently in use by another application.\n\t\t\"PermissionError: [Errno 13] Permission denied...\"")
print("----------------------------------------------------------------------------------------------------------------------------")
print()
    
if len(argv) != 3:
    print()    
    print("----------------------------------------------------------------------------------------------------------------------------")
    print("ERROR: Provide Arguments. Please provide the name of the input file and then the name of the outputfile")
    print("----------------------------------------------------------------------------------------------------------------------------")
    exit()

filename =  str(argv[1])

#Read the existing CSV file and store its content
try:
    in_file = open(filename, mode ='r') 
except OSError:
    print("----------------------------------------------------------------------------------------------------------------------------")
    print("ERROR: Filenames/Location. Please ensure paths to files are correct and are enclosed in \"\".")
    print("----------------------------------------------------------------------------------------------------------------------------")
    exit()
with in_file:
    csvFile = csv.reader(in_file)
    data = list(csvFile)
    
num_entry = len(data) # Number of rows
# Process the data
# Remember indexing starts at [0][0]
# [rows][cols]

# f_lat[] -> latitude col (data[i][18])
# f_long[] -> longitude col (data[i][19])
closest_obj = [[-1]]    # 2D list containing the list of nodes/equipment withing grouping distance
min_dist = [-1]         # Colum Header

# min_dist could be removed as this information doesn't need to be stored

f_lat = []              # Float in radians
f_long = []             #
missing_data = []   

f_lat.append(0)
f_long.append(0)

for i in range(1,num_entry):
    if data[i][18] != "":
        f_lat.append(float(data[i][18]))
        f_long.append(float(data[i][19]))
    else:
        missing_data.append(i)      # Add index to missing data
        f_lat.append(0)
        f_long.append(0)

# Warn about issues with datasets, including equipment with not listed location
print("Missing indices:")    
print(missing_data)
print()

# For each entry calculate distances to make lists other equipment within grouping threshold
for i in range(1,num_entry):
    # Check distance from every other entry
    min_dist.append(MAX_GROUP_DIST)
    closest_obj.append([])
    if i not in missing_data:
        for j in range(1, num_entry):
            if j not in missing_data and j != i:
                dist_calc = find_dist(f_lat[i],f_long[i],f_lat[j],f_long[j],)
                
                if dist_calc < MAX_GROUP_DIST:
                    if dist_calc < min_dist[i]:
                        min_dist[i] = dist_calc
                    closest_obj[i].append(j)

#Fix Directions
for i in range(1, num_entry):
    temp = data[i][17].upper()
    # REPLACE:
    # temp = data[i][5].upper()
    if len(temp) == 0:
        dir.append("")
    elif len(temp) == 1:
        dir.append(temp)
    else:
        #Find substrings and append
        dir.append("")
        if "EAST" in temp:
            dir[i] = dir[i] + "E"
        elif "WEST" in temp:
            dir[i] = dir[i] + "W"
            
        # Were not needed and inconsistently used in document, these are only confirmed against the road chainage markers
        
        #elif "NORTH" in temp:
            #dir[i] = dir[i] + "N"
        #elif "SOUTH" in temp:
            #dir[i] = dir[i] + "S"    

#Prepare Junction data for group ID
#Read the existing CSV file and store its content
try:
    junctions_file = open(filename_junctions, mode ='r') 
except OSError:
    print("----------------------------------------------------------------------------------------------------------------------------")
    print("ERROR: Filenames/Location. Please ensure path to junctions file is correct and are enclosed in \"\".")
    print("----------------------------------------------------------------------------------------------------------------------------")
    exit()
    
for source in range(0, len(junctions)):
    # Determine if in a pair
    junctiondists.append(-1)
    if int(junctions[source]["Number Junctions"]) == 2:
        for target in range(0, len(junctions)):
            if junctions[target]["Junction"] == junctions[source]["Junction"] and junctions[target]["Long"] != junctions[source]["Long"]:
                # These are together
                # Get the distances between matching junctions
                junctiondists[source] = find_dist(float(junctions[source]["Lat"]), float(junctions[source]["Long"]), float(junctions[target]["Lat"]), float(junctions[target]["Long"]))
                break
    #print([source], end=", ")
    #print(junctions[source], end=", ")
    #print(junctiondists[source])


#Prepare Junction data for group ID
filename_markers = "M7_N7.csv"
#Read the existing CSV file and store its content
try:
    markers_file = open(filename_markers, mode ='r') 
except OSError:
    print("----------------------------------------------------------------------------------------------------------------------------")
    print("ERROR: Filenames/Location. Please ensure path to junctions file is correct and are enclosed in \"\".")
    print("----------------------------------------------------------------------------------------------------------------------------")
    exit()
with markers_file:
    markerCSV = csv.reader(markers_file)
    markers = list(markerCSV)    

# Create and assign group numbers
curr_group = 1
groups = ["Group ID"] #initialized list

for i in range(1,num_entry):
    # Not grouped by default
    if closest_obj[i] == []:
        groups.append(form_groupID(i)) # Not grouped by default
        curr_group += 1
        
    ## belongs in a group and the index of the neighbour has not been given a group yet
    elif all(idx > len(groups) for idx in closest_obj[i]):
        # create new group
        groups.append(form_groupID(i)) # New Group
        curr_group += 1
    
    # Join existing group if in same direction
    else:
        found_flag = False
        for idx in closest_obj[i]:
            if dir[idx] == dir[i]:
                # If in the same direction then they are compatible for grouping
                groups.append(str(groups[closest_obj[i][0]]))   # Same group as closest 
                found_flag = True                               # No issue with choosing the first object as the order in which they are added is consistent for all groups
                break
        if not found_flag:
            # If you get here that means that although nodes are near enough to it none of them are grouped with it (maybe yet)
            # and therefore create new grouping separate
            
            groups.append(form_groupID(i)) # New Group
            curr_group += 1
    
data[0].append('Group ID')

# Add the new column values to the remaining rows of the data
for i in range(1, num_entry):
    data[i].append(groups[i])

# For testing: OutputCSV.csv
# Write the updated data to new/old CSV file
filename =  str(argv[2])
with open(filename, 'w', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerows(data)
''''''

print()
print("Task completed with no errors :)")