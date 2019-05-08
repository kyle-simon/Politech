import json
import sys
# from PoliTech.api.constants import STATES

def json_read(filename):
   with open(filename) as f_in:
        data = json.load(f_in)

        for elem in data["features"]:
            coordinates = elem["geometry"]["coordinates"]
            elem["precinct_shape"] = elem.pop("geometry")
            if elem["precinct_shape"]["type"] == "MultiPolygon":
                elem["precinct_shape"]["coordinates"] = coordinates
            else:
                elem["precinct_shape"]["type"] = "MultiPolygon"
                elem["precinct_shape"]["coordinates"] = [coordinates]
            state = elem["properties"]["STATEFP10"]
            description = elem["properties"]["NAMELSAD10"]
            del elem["properties"]
            elem["state"] = state
            elem["description"] = description
            del elem["type"]
        return(data)

def json_write(dict, filename):
    with open(filename,'w+') as f_out:
        f_out.write(json.dumps(dict["features"], indent=4))

if (len(sys.argv) != 3):
    sys.exit(0)

if __name__ == "__main__":
    print("Parsing...")
    my_data = json_read(sys.argv[1])
    json_write(my_data, sys.argv[2])
    print("Done")
