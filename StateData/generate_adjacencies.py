import json
import pysal as ps

res = []
def getNeightborIDs(index, inds):
    for i in inds:
        res.append({"from_precinct":index,"to_precinct":i})

def json_write(dict, filename):
    with open(filename,'w+') as f_out:
        f_out.write(json.dumps(dict, indent=4))

filename = "NC"

# Get centers and neighbors
w = ps.lib.weights.Queen.from_shapefile("Data/"+filename+"/"+filename+".shp")
n = w.neighbors

f = ps.lib.io.open("Data/"+filename+"/"+filename+".shp")
p = f.read()


# Populate the DB
with open("Data/"+filename+"/"+filename + ".json") as json_file:
    json_data = json.load(json_file)
    features = json_data["features"]
    neighbors = {}  # Maps index to list of neighbor indexes
    count = 0
    # Handle geometry
    for precinct in features:
        neighbors[count] = n[count]
        count += 1
    count = 0
    data={}
    for precinct in features:
        getNeightborIDs(count, neighbors[count])
        count += 1
    json_write(res, "NC_adjacencies.json")
