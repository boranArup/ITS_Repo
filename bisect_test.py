from sys import argv
from math import sin, acos, cos, sqrt, radians, degrees, atan2
import csv
import bisect

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
    

x = find_angle(-1,-1,-0,-0,3,-3)
print(x)
x = find_angle(-1,1,-0,-0,-5,-4)
print(x)
x = find_angle(-1,-1,0,-0,-0,1)
print(x)
x = find_angle(1,-1,-0,0,-1,0)
print(x)
x = find_angle(-1,-0,-0,-0,-0,-1)
print(x)
x = find_angle(1,1,0,-0,-1,-1)
print(x)
