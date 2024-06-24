import re
import csv

# Cuts out all non relavent lines
filename_out = "junctions - Copy.csv"
filename_in = "junctions.csv"
#filename_in = "..\..\Downloads\IREJunctions\planet_-10.593_51.349_e3b7e9d5.osm (2).text"

with open(filename_out, mode ='w', encoding="utf-8") as wfile:
    with open(filename_in, mode ='r', encoding="utf-8") as rfile:
        for line in rfile:
            if  ",NI," in line:
                pass # Do not include
            else:
                row = line.split(",")
                if float(row[0]) < 53.3 and row[0] != 0:
                    wfile.write(line)
        
print("Task completed :)")

'''
with open(filename, 'w', newline='') as out_file:
    writer = csv.writer(out_file)
    writer.writerows(data)
    
    csvFile = csv.reader(in_file)
    data = list(csvFile)
'''