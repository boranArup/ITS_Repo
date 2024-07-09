#import re
from sys import argv
from math import sin, cos, sqrt, radians, degrees, atan2
import csv
import bisect

# Define the setpoint for maximum distance considered as a grouping of equipments between two objects
# Note: As long as a node is close enough to any of the nodes/equipment in a group it joins the group even if distance
# to some nodes is larger than setpoint!
MAX_GROUP_DIST = 0.035
data = [[]]
junctions = [{}]
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

def to_degree_form(x,y):
    x = "53°18'59.49\"N", "6°22'33.57\"W"
    pass


    
filename =  "Final data.csv"

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
    
coords = [[]]

lendata = 1
while data[lendata][3] != "":
    
    x = data[lendata][3].replace("Â","")
    print(x, end=" , ")
    x = x.replace("°","-")
    x = x.replace('\'','-')
    x = x.replace('"','')
    latitude = x

    y = data[lendata][4].replace("Â","")
    print(y)
    y = y.replace("°","-")
    y = y.replace('\'','-')
    y = y.replace('"','')
    longitude = y


    E = 'E' in longitude
    #print(longitude, "  +++")
    d, m, s = map(float, longitude[:-1].split('-'))
    longitude = round((d + m / 60. + s / 3600.) * (1 if E else -1),6)

    N = 'N' in latitude
    #print(latitude, "  +++")
    d, m, s = map(float, latitude[:-1].split('-'))
    latitude = round((d + m / 60. + s / 3600.) * (1 if N else -1),6)

    #y =
    coords.append([latitude,longitude])
    
    lendata += 1

print(coords)
print()
print(len(coords))
print(lendata)
    