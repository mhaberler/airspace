import json
from shapely.geometry import shape, Point

transition_level = 10000 # ft, Austria

ft_to_m = 0.3048

fn = "/srv/data/geojson/airspace/austria_at.json"


def pres2alt(pressure):
    '''
    Determine altitude from site pressure.

    Parameters
    ----------
    pressure : numeric
        Atmospheric pressure. [Pa]

    Returns
    -------
    altitude : numeric
        Altitude above sea level. [m]

    Notes
    ------
    The following assumptions are made

    ============================   ================
    Parameter                      Value
    ============================   ================
    Base pressure                  101325 Pa
    Temperature at zero altitude   288.15 K
    Gravitational acceleration     9.80665 m/s^2
    Lapse rate                     -6.5E-3 K/m
    Gas constant for air           287.053 J/(kg K)
    Relative Humidity              0%
    ============================   ================

    References
    -----------
    .. [1] "A Quick Derivation relating altitude to air pressure" from
       Portland State Aerospace Society, Version 1.03, 12/22/2004.
    '''

    alt = 44331.5 - 4946.62 * pressure ** (0.190263)

    return alt

press = 919.8454
pa_ft = pres2alt(press*100)/ft_to_m
fl = int(pa_ft/100)
print(f"pressure altitude {int(pa_ft)}ft FL{fl}")

# pressire x temp x alt -> pressure at sea level
# https://gist.github.com/cubapp/23dd4e91814a995b8ff06f406679abcf
def adjust_pressure(aap,atc,hasl):
    # Actual atmospheric pressure in hPa
    aap = 990 
    # Actual temperature in Celsius
    atc = 10
    # Height above sea level
    hasl = 500

    # Adjusted-to-the-sea barometric pressure
    a2ts = aap + ((aap * 9.80665 * hasl)/(287 * (273 + atc + (hasl/400))))

    # in standard places (hasl from 100-800 m, temperature from -10 to 35) 
    # is the coeficient something close to hasl/10, meaning simply 
    # a2ts is about  aap + hasl/10
    return a2ts

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
    return above_ab and below_at



# load GeoJSON file containing sectors
with open(fn) as f:
    js = json.load(f)

# construct point based on lon/lat returned by geocoder
point = Point(10, 47)

# Stiwoll
point = Point(15.21197450, 47.12919800)

alt_ft = pa_ft 

alt_ft = 10000

# check each polygon to see if it contains the point
for feature in js['features']:
    name = feature["properties"]["N"]
    at = feature["properties"]["AT"]
    at_u = feature["properties"]["AT_U"]
    ab = feature["properties"]["AB"]
    ab_u = feature["properties"]["AB_U"]
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        within = within_airspace(alt_ft,ab, ab_u,  at, at_u)

        print(f"Found containing polygon: {name} {ab}{ab_u} {at}{at_u} within({alt_ft}ft)={within}")
