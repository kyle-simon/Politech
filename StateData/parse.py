import json
import sys
# from PoliTech.api.constants import STATES

def json_read(filename):
   with open(filename) as f_in:
        data = json.load(f_in)

        for elem in data["features"]:
            elem["geometry"]["type"] = "MultiPolygon"
            state = elem["properties"]["STATEFP10"]
            description = elem["properties"]["NAMELSAD10"]
            del elem["properties"]
            elem["state"] = state
            elem["description"] = description
        return(data)

def json_write(dict, filename):
    with open(filename,'w+') as f_out:
        f_out.write(json.dumps(dict, indent=4))

if (len(sys.argv) != 3):
    sys.exit(0)

if __name__ == "__main__":
    print("Parsing...")
    my_data = json_read(sys.argv[1])
    json_write(my_data, sys.argv[2])
    print("Done")
    # print(json.dumps(my_data["features"][0], indent=4))



# {
#     "precinct_shape": {
#             "type": "Feature",
#             "geometry": {
#                 "type": "MultiPolygon",
#                 "coordinates": [
#                     [
#                         [
#                             [
#                                 -77.042158,
#                                 36.239931
#                             ],
#                             [
#                                 -76.963054,
#                                 36.215963
#                             ],
#                             [
#                                 -76.96133,
#                                 36.212988
#                             ],
#                             [
#                                 -76.958024,
#                                 36.209898
#                             ],
#                             [
#                                 -76.950832,
#                                 36.200791
#                             ],
#                             [
#                                 -77.042158,
#                                 36.239931
#                             ]
#                         ]
#                     ]
#             ]
#         }
#     },
#     "state": "37",
#     "description": "Voting District M1"
# }


# 'MultiPolygon(((-77.042158 36.239931, -76.963054 36.215963, -76.96133 36.212988, -76.958024 36.209898,-76.950832 36.200791,-77.042158 36.239931)))';
# insert into `api_precinct`(precinct_shape, state, description) VALUES (ST_GeomFromText(@g), "NY", "test");
