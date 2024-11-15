# Module with all universal constants needed to calculations
import datetime
import spiceypy

from .utilities import kernels_load

kernels_load(["../kernels/lsk/naif0012.tls"])

# Today date (at midnight) in Year - month - dayT00:00:00 format
TODAY_DATE = datetime.datetime.today().strftime("%Y-%m-%dT00:00:00")


# Today Date as ephemeris time (ET)
ET_TODAY_DATE_MIDNIGHT = spiceypy.utc2et(TODAY_DATE)

# How many Kilometers in AU
AU_TO_KM = 149_597_871

# How many seconds in hour
HOUR_TO_SECONDS = 3600


NAIF_PLANETS_ID = {
    "Sun": 10,
    "Venus": 299,
    "Earth": 399,
    "Moon": 301,
    "Mars": 4,
    "Jupiter": 5,
    "Saturn": 6,
    "Uran": 7,
    "Neptun": 8,
    "Ceres": 2000001,
    "SSB": 0,  # Solar System Barycentre
}

PLANETS_COLOR = {
    "Sun": "gold",
    "Mercury": "maroon",
    "Venus": "palegoldenrod",
    "Earth": "mediumseagreen",
    "Moon": "silver",
    "Mars": "tomato",
    "Jupiter": "burlywood",
    "Saturn": "darkkhaki",
    "Uran": "paleturquoise",
    "Neptun": "blue",
}

PLANETS_SIZE = {
    "Sun": 20,
    "Mercury": 8,
    "Venus": 11,
    "Earth": 12,
    "Moon": 6,
    "Mars": 10,
    "Jupiter": 15,
    "Saturn": 17,
    "Uran": 18,
    "Neptun": 19,
}
