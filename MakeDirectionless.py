# Personal paths for use
#  C:/Users/leonardo.boran/AppData/Local/miniforge3/envs/arup-env/python.exe c:/Users/leonardo.boran/MakeDirectionless.py ".\OneDrive - Arup\\TestCoordsCSV.csv" x

#TODO: CLEAN UP BOTH VERSIONS!

from sys import argv
from math import sin, asin, cos, sqrt, radians, degrees, pow, atan2
import csv

# Define the setpoint for maximum distance considered as a grouping of equipments between two objects
# Note: As long as a node is close enough to any of the nodes/equipment in a group it joins the group even if distance
# to some nodes is larger than setpoint!
MAX_GROUP_DIST = 0.1

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
        f_lat.append(radians(float((data[i][18]))))
        f_long.append(radians(float((data[i][19]))))
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
                diff_lat = (f_lat[j]-f_lat[i])
                diff_long = (f_long[j]-f_long[i])
                a = (sin(diff_lat / 2) * sin(diff_lat / 2) +
                        cos(f_lat[j]) * cos((f_lat[i])) *
                        sin(diff_long / 2) * sin(diff_long / 2))
                b = atan2(sqrt(a), sqrt(1-a))
                dist_calc = 12742 * b
                
                if dist_calc < MAX_GROUP_DIST:
                    if dist_calc < min_dist[i]:
                        min_dist[i] = dist_calc
                    closest_obj[i].append(j)
 
# Create and assign group numbers
curr_group = 1
groups = ["Group ID"] #initialized list

for i in range(1,num_entry):
    # Not grouped by default
    if closest_obj[i] == []:
        groups.append(str(curr_group)+"_Solo") # Not grouped by default
        curr_group += 1
        
    ## belongs in a group and the index of the neighbour has not been given a group yet
    elif all(idx > len(groups) for idx in closest_obj[i]):
        # create new group
        groups.append(str(curr_group)+"_") # New Group
        curr_group += 1
    
    # Join existing group
    else:
        groups.append(str(curr_group) + "_") # New Group
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
'''
# Write the updated data to new/old CSV file
filename = prefix + str(argv[2])
with open(filename, 'w', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerows(data)
'''