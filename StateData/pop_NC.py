import json
import pysal as ps


def getNeighborJSON(inds, precs):
    to_return = "{adjacencies:[ "
    first = True
    print(inds)
    for i in inds:
        # if (districts[i] != "0"):
        #     if (first):
        #         first = False
        #     else:
        #         to_return += ", "
        to_return += ("" + str(precs[i]["properties"]) + "")
    to_return += " ]}"
    return to_return


filename = "NC"
statename = "North Carolina"

# Get centers and neighbors
w = ps.lib.weights.Queen.from_shapefile(filename+".shp")
n = w.neighbors

f = ps.lib.io.open(filename + ".shp")
p = f.read()


# Populate the DB
with open(filename + ".json") as json_file:
    json_data = json.load(json_file)
    features = json_data["features"]
    precincts = {}  # Maps index to name
    neighbors = {}  # Maps index to list of neighbor indexes
    districts = {}  # Maps index to districtID
    centers = {}  # Maps index to center
    areas = {}  # Maps index to area
    count = 0
    # Handle geometry
    for precinct in features:
        neighbors[count] = n[count]
        count += 1
    count = 0
    data={}
    for precinct in features:
        neighborJSON = getNeighborJSON(neighbors[count], features)
        count += 1
    print(json.dumps(neighborJSON,indent=4))
