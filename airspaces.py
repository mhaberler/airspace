import json
from shapely.geometry import shape, Point


def  within_airspace(alt_ft, abs, ab_u,  ats, at_u):
    fl = int(alt_ft/100)
    above_ab = False
    below_at = False
    ab = int(abs)
    at = int(ats)
    if ab_u == "F":
        above_ab = alt_ft > ab
    if ab_u == "FL":
        above_ab = fl > ab

    if at_u   == "F":
        below_at = alt_ft < at
    if at_u   == "FL":
        below_at = fl < at
    return (above_ab, below_at)


fn = "/srv/data/geojson/airspace/austria_at.json"

# load GeoJSON file containing sectors
with open(fn) as f:
    js = json.load(f)


# Stiwoll
# point = Point(15.21197450, 47.12919800)
# Thalerhof

point = Point(15.460366012549866,46.95808587082531)

alt_ft = 7100

print(f"position={point}, altitude {alt_ft}ft:")

# check each polygon to see if it contains the point
for feature in js['features']:
    name = feature["properties"]["N"]
    at = feature["properties"]["AT"]
    at_u = feature["properties"]["AT_U"]
    ab = feature["properties"]["AB"]
    ab_u = feature["properties"]["AB_U"]
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        (above, below) = within_airspace(alt_ft,ab, ab_u,  at, at_u)
        if above and below:
            print(f"within; '{name}' {ab}{ab_u} {at}{at_u}", feature["properties"])
        else:
            if above:
                print(f"above '{name}' {ab}{ab_u} {at}{at_u}", feature["properties"])
            if below:
                print(f"below '{name}' {ab}{ab_u} {at}{at_u}", feature["properties"])        