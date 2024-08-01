# import module
from geopy.geocoders import Nominatim
from csv import reader, writer

def chartoidx(c):
    c = c.upper()
    if len(c) == 1:
        num = ord(c)
        if  num > 64:
            return num - 65
    return int(c)

#Read the existing CSV file and store its content
#\\global\europe\Dublin\jobs\262000\262215-01\7. Site Related Activities\7-07 Site Instructions\7-07-06 Change Orders\Change Order Assets Lists\7-09-05-01 DWS\Overall DWS_Version4.xlsx
filename = input("Enter input filepath: ")
data = []
print()
print(filename)
print()

try:
    in_file = open(filename, mode ='r',newline="\n") 
except OSError:
    print("----------------------------------------------------------------------------------------------------------------------------")
    print("ERROR: Filenames/Location. Please ensure paths to files are correct and are enclosed in \"\".")
    print("----------------------------------------------------------------------------------------------------------------------------")
    exit()
with in_file:
    csvFile = reader(in_file,delimiter=",",quotechar='"')
    data = list(csvFile)
    
print("Insert letter column or number starting at index 0.\nOnly letters up to z supported.\n")
idc = chartoidx(input("ID Column: "))
yc = 0.0   # Initialised for scope
xc = chartoidx(input("Column Num Lat: "))
tempin = input("(Can leave blank if straight after Lat)\nColumn Num Long: ")
if tempin == "":
    yc = xc + 1
else : 
    yc = chartoidx(tempin)
    
# initialize Nominatim API
geolocator = Nominatim(user_agent="http")
location = geolocator.reverse(data[11][xc]+","+data[11][yc])
address = location.raw['address']
county = address.get('county')
print('County : ', county,data[11][1])


ID_w_county = []

for line in data[1:]:
    location = geolocator.reverse(line[xc]+","+line[yc])

    address = location.raw['address']

    # traverse the data
    county = address.get('county')
    county = county.replace("County ","")
    print('County : ', county)
    ID_w_county.append([line[idc],county])

out_file = filename.replace(".csv","_output.csv")

# Write a csv with location id, county
with open(out_file, 'w', newline='') as out_file:
    writer = writer(out_file)
    writer.writerows(ID_w_county)
    
    ''''''