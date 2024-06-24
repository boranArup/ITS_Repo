# Personal paths for use
#  C:/Users/leonardo.boran/AppData/Local/miniforge3/envs/arup-env/python.exe "c:/Users/leonardo.boran/OneDrive - Arup/ITS_Repo/AutomatedGroupingDir.py" TestCoordsCSV.csv OutputCSV.csv

from sys import argv
from math import sin, asin, cos, sqrt, radians, degrees, pow, atan2
import csv


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


#M7E-J9J9A-22141E-AID
# Prepare ID string
def form_groupID(idx):
    id = ""
    min = [100,100]
    near_junctions = ["",""]
    for junction in junctions:
        dist = find_dist(float(junction[0]),float(junction[1]),f_lat[idx],f_long[idx])
        if dist < min[0]:
            min[0] = dist
            near_junctions[0] = junction[2]
        elif dist < min[1]:
            min[1] = dist
            near_junctions[1] = junction[2]
    # TODO: FIX FLOATING JS
    id = id + "J" + near_junctions[0] + "J" + near_junctions[1]
    print(id)
    #id.append()
    #id.append("_")
    return
# Define the setpoint for maximum distance considered as a grouping of equipments between two objects
# Note: As long as a node is close enough to any of the nodes/equipment in a group it joins the group even if distance
# to some nodes is larger than setpoint!
MAX_GROUP_DIST = 0.035
data =[[]]
junctions =[[]]

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
#prefix
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
closest_obj = [[-1]]    # 2D list containing the list of nodes/equipement withing grouping distance
min_dist = [-1]         # Collum Header
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
dir = ["Direction"]
for i in range(1, num_entry):
    temp = data[i][17].upper()
    if len(temp) == 0:
        dir.append("N/A")
    elif len(temp) < 3:
        dir.append(temp)
    else:
        #Find substrings and append
        dir.append("")
        if "NORTH" in temp:
            dir[i] = dir[i] + "N"
        if "SOUTH" in temp:
            dir[i] = dir[i] + "S"    
        if "EAST" in temp:
            dir[i] = dir[i] + "E"
        if "WEST" in temp:
            dir[i] = dir[i] + "W"    
print(dir)       
print()

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

# Create and assign group numbers
curr_group = 1
groups = ["Group ID"] #initialized list

for i in range(1,num_entry):
    # Not grouped by default
    if closest_obj[i] == []:
        form_groupID(i)
        groups.append(str(curr_group)+"_"+dir[i]+"_Solo") # Not grouped by default
        curr_group += 1
        
    ## belongs in a group and the index of the neighbour has not been given a group yet
    elif all(idx > len(groups) for idx in closest_obj[i]):
        # create new group
        form_groupID(i)
        groups.append(str(curr_group)+"_"+dir[i]) # New Group
        curr_group += 1
    
    # Join existing group if in same direction
    else:
        #TODO:Go through group to ensure that items grouped with are heading the same direction!
        found_flag = False
        for idx in closest_obj[i]:
            if dir[idx] == dir[i]:
                # If in the same direction then they are compatible for grouping
                form_groupID(i)
                groups.append(str(groups[closest_obj[i][0]]))   # Same group as friend
                found_flag = True                               # No issue with choosing the first object as the order in which they are added is consistent for all groups
                break
        if not found_flag:
            # If you get here that means that although nodes are near enough to it none of them are grouped with it (maybe yet)
            # and therefore create new grouping seperate
            form_groupID(i)
            groups.append(str(curr_group) + "_" + dir[i]) # New Group
            curr_group += 1
        
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

print(junctions)
   
''''''