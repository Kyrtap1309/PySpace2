import spiceypy
import numpy as np

from ..utilities.utilities import get_utc_time, kernels_load
from ..utilities.kernels_constants import REQUIRED_FILES



class Ceres:
    def __init__(self, date: dict) -> None:
        self._kernels_load()
        self._ceres_init(date)

    def _kernels_load(self) -> None:
        """
        Function to load kernels
        """
        kernels = REQUIRED_FILES[self.__class__.__name__.lower()]
        kernels_load(kernels)

    def _ceres_init(self, date: dict) -> None:
        # Initialization of UTC time
        self._utc_time_str = get_utc_time(date).strftime("%Y-%m-%dT%H:%M:%S")
        # Initialization of ET time
        self._et_time = spiceypy.utc2et(self._utc_time_str)

        # Calculating a ceres state vector and time of light's travel between
        # the ceres and the sun
        # Using spkgeo function with parametres:
        # targ = 2000001 - NAIF ID of the planet (The Ceres in this case)
        # that state vector is pointing
        # et  - Reference time of calculations
        # ref = 'ECLIPJ2000' - An Ecliptic Plane used in calculations
        # obs = 10 - NAIF ID of the object (The Sun in this case)
        # which is the beggining of state vector
        _planet_state_vector, _ = spiceypy.spkgeo(
            targ=2000001, et=self._et_time, ref="ECLIPJ2000", obs=10
        )
        _, GM_sun = spiceypy.bodvcd(bodyid=10, item="GM", maxn=1)
        GM_sun = GM_sun[0]

        # Orbital elements of Ceres
        _ceres_planet_elements = spiceypy.oscltx(
            _planet_state_vector, self._et_time, GM_sun
        )

        self.ceres_semi_major_au = spiceypy.convrt(
            _ceres_planet_elements[9], inunit="km", outunit="AU"
        )
        self.ceres_perihelion_au = spiceypy.convrt(
            _ceres_planet_elements[0], inunit="km", outunit="AU"
        )
        self.ceres_ecentricity = _ceres_planet_elements[1]

        # Create readable (in degrees) representation of angular values
        self.ceres_inclination_deg = np.degrees(_ceres_planet_elements[2])
        self.ceres_longitude_asc_node_deg = np.degrees(_ceres_planet_elements[3])
        self.ceres_arg_perihelion_deg = np.degrees(_ceres_planet_elements[4])

        # Ceres orbital period
        self.ceres_orbital_period_years = _ceres_planet_elements[10] / (86400 * 365)
        