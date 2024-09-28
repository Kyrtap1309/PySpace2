# Module with all universal constants needed to calculations
import datetime
import spiceypy

from .utilities import get_furnsh_kernel_path

spiceypy.furnsh(get_furnsh_kernel_path("../../kernels/lsk/naif0012.tls"))

# Today date (at midnight) in Year - month - dayT00:00:00 format
TODAY_DATE = datetime.datetime.today().strftime("%Y-%m-%dT00:00:00")


# Today Date as ephemeris time (ET)
ET_TODAY_DATE_MIDNIGHT = spiceypy.utc2et(TODAY_DATE)

# How many Kilometers in AU
AU_TO_KM = 149_597_871
