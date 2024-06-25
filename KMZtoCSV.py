#Convert kmz/kml to csv
import re

# Cuts out all non relavent lines
filename_in = "M7_N7.csv"
filename_out = "Output.txt"
#filename_in = "..\..\Downloads\IREJunctions\planet_-10.593_51.349_e3b7e9d5.osm (2).text"

with open(filename_out, mode ='w', encoding="utf-8") as wfile:
    with open(filename_in, mode ='r', encoding="utf-8") as rfile:
        for line in rfile:
            
            newline = ""
            skip = 4
            
            for char in line:
                if char == ",":
                    skip = 5
                    newline += char
                    
                if skip == 0:
                    newline += char
                    
                else:
                    skip -= 1


            wfile.write(newline)

            
            '''
                if print_normal:
                    newline = newline + char
                else:
                    if waitfornum:
                        if char == "(":
                            waitfornum = False
                    else:
                        if char == ")":
                            newline = newline + " " + temp
                            print_normal = True
                        elif char == " ":
                            secondnum = True
                            newline = newline
                        else:
                            if secondnum:
                                newline = newline + char
                            else:
                                temp = temp + char
            print(newline, end="")
            wfile.write(newline)
        #print()
        '''
print("Task completed :)")