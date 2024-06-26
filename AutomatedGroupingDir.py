# Personal paths for use
#  C:/Users/leonardo.boran/AppData/Local/miniforge3/envs/arup-env/python.exe "c:/Users/leonardo.boran/OneDrive - Arup/ITS_Repo/AutomatedGroupingDir.py" TestCoordsCSV.csv OutputCSV.csv

from sys import argv
from math import sin, acos, cos, sqrt, radians, degrees, atan2
import csv
import bisect

# Define the setpoint for maximum distance considered as a grouping of equipments between two objects
# Note: As long as a node is close enough to any of the nodes/equipment in a group it joins the group even if distance
# to some nodes is larger than setpoint!
MAX_GROUP_DIST = 0.035
data = [[]]
junctions = [[]]
junctiondists = []
markers = [[]]
dir = ["Direction"]


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
    
    angle = find_angle(float(j1[0]),float(j1[1]),float(j2[0]),float(j2[1]),float(j3[0]),float(j3[1]))
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
        dist = find_dist(float(junctions[i][0]),float(junctions[i][1]),f_lat[idx],f_long[idx])
        if dist > max_between_junct:
            i = -1
            dist = max_between_junct
        bisect.insort(minjuncts, [ dist, i])
            
    # Junctions
    # TODO: ADAPT THIS SECTION TO YOUR ALGORITHM 
    print("Near id "+ str(minjuncts[0][1]), end=" ")
    if minjuncts[0][1] == -1 or markerdist[0] >= 0.75:
        # There is no near junction
        id = "NOT-IN-SCOPE"
        print(data[idx][18], end=" ")
        print(data[idx][19], end="  ")
        print(id, end="  ")
        print(minjuncts[0][0])
        
        return(id) 
    
    else:
        # Calculate if between junction pair
        dist0 = find_dist(float(junctions[minjuncts[0][1]][0]),float(junctions[minjuncts[0][1]][1]),f_lat[idx],f_long[idx])
        dist1 = find_dist(float(junctions[minjuncts[1][1]][0]),float(junctions[minjuncts[1][1]][1]),f_lat[idx],f_long[idx])
        
        # Default to using 0 and 1 as normal
        chosen_idx = minjuncts[1][1]
        
        # Check if 0 and 1 are *NOT* two ends of a junction and the equipment is within these bounds
        print(junctions[minjuncts[0][1]], end=" ")
        print(", Distance between junctions: ", end=" ")
        print(junctiondists[minjuncts[0][1]], end=" ")
        
        print()
        if junctiondists[minjuncts[0][1]] < dist0 or junctiondists[minjuncts[0][1]] < dist1:
    
            print("Not within junction")        
            # Check if 0 and 1 have same junction name
            if junctions[minjuncts[0][1]][2] == junctions[minjuncts[1][1]][2]:
                print("Has the same name tho")
                
                # Check if 2 is a suitable junction or is the following junction nearer by and being incorrectly chosen
                i = 0
                
                while same_dir(junctions[minjuncts[i][1]],junctions[minjuncts[i+1][1]],junctions[minjuncts[i+2][1]]):
                    # Go to the next junction and recheck if its in the same direction
                    i += 1
              
                # Not in the same direction as the two junction parts use this
                chosen_idx = minjuncts[i+2][1]   
        else:
            print("Within Junction")
            
        id = id + "J" + junctions[minjuncts[0][1]][2] + "J" + junctions[chosen_idx][2]

    
    '''      
    if minjuncts[0][1] == "":
        id = id + "NA"
    elif minjuncts[1][1] == "":
        id = id + "J" + minjuncts[0][1] + "J" +minjuncts[0][1]
    else:
        id = id + "J" + minjuncts[0][1] + "J" + minjuncts[1][1]
    '''  
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
    id = id + str(lenghtofroad) + used_dir
    
    if "JEND" in id or "JSTART" in id:
        id = "NOT-IN-SCOPE"
        
    print(data[idx][18], end=" ")
    print(data[idx][19], end="  ")
    print(id, end="  ")
    print(minjuncts[0][0])
    
    #TODO: VERIFY JUNCTION MATCHING TO BE CORRECT, JUDGE THE J11J11 AND NA CATEGORIZED ONES
    #TODO: VERIFY HEADING, ARE THE ROAD MARKERS GOOD ENOUGH?
    
    return(id)


# CHECK FOR ERRORS IN INPUT:
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

prefix = ".\OneDrive - Arup\\"
filename =  str(argv[1])

# Basic read and print out full csv
'''   
with open(filename, mode ='r') as file:
csvFile = csv.reader(file)
for lines in csvFile:
        print(lines)
'''

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

# data[][18] -> latitude col
# data[][19] -> longitude col
closest_obj = [[-1]]    # 2D list containing the list of nodes/equipment withing grouping distance
min_dist = [-1]         # Colum Header
# TODO:Remove min_dist as this information doesn't need to be stored
f_lat = []              # Float in radians
f_long = []             #
missing_data = []   

f_lat.append(0)
f_long.append(0)


for i in range(1,num_entry):
    if data[i][18] != "":
        f_lat.append((float((data[i][18]))))
        f_long.append((float((data[i][19]))))
    else:
        missing_data.append(i)      # Add index to missing data
        f_lat.append(0)
        f_long.append(0)
        
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
        #elif "NORTH" in temp:
            #dir[i] = dir[i] + "N"
        #elif "SOUTH" in temp:
            #dir[i] = dir[i] + "S"    
            #TODO: DO YOU WANT TO TRANSLATE THESE TO EAST AND WEST???

#print(dir)       
#print()

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
        #TODO:Go through group to ensure that items grouped with are heading the same direction!
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
    
    # UNCOMMENT FOR INFO ON ALL PAIRINGS IN A MAKESHIFT TABLE
    '''
    print("Group No. : " +  "%15s" %str(groups[i]) + ",\t Index : " + str(i) + ",\t Neighbour : " + "%25s" % str(closest_obj[i]) + ",\t ID : " +  "%11s" %str(data[i][1]), end=" | ")
    #print("ID : " +  "%23s" %str(data[i][0]), end=" | ")
    for item in closest_obj[i]:
        print("%11s" %data[item][1], end=", ")
    print()    
#print(closest_obj)
print()    
print(groups)
print()    
print(len(groups))
'''

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

print()
print("Task completed with no errors :)")