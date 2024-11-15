import spiceypy
import numpy as np

from ..utilities.utilities import get_utc_time, kernels_load
from ..utilities.kernels_constants import REQUIRED_FILES
from ..utilities.constants import NAIF_PLANETS_ID


class Orbit:
    def __init__(self, date: dict, chosen_planet: str) -> None:
        """
        Initialize the class with date to calculate orbit properties.

        Parameters:
        -----------
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        chosen_planet : str
            Chosen planet for the calculations.
        """

        self._kernels_load()
        self._orbit_init(date, chosen_planet)

    def _kernels_load(self) -> None:
        """
        Function to load kernels
        """
        kernels = ["../kernels/" + kernel for kernel in REQUIRED_FILES[self.__class__.__name__.lower()]]
        kernels_load(kernels)

    def _orbit_init(self, date: dict, chosen_planet: str) -> None:
        """
        Initialize the Orbit object with the provided date.

        Parameters:
        -----------
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        chosen_planet : str
            Chosen planet for the calculations
        """

        # Initialization of UTC time
        self._utc_time_str = get_utc_time(date).strftime("%Y-%m-%dT%H:%M:%S")
        # Initialization of ET time
        self._et_time = spiceypy.utc2et(self._utc_time_str)

        naif_id = NAIF_PLANETS_ID[chosen_planet.capitalize()]

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
            targ=naif_id, et=self._et_time, ref="ECLIPJ2000", obs=10
        )
        _, GM_sun = spiceypy.bodvcd(bodyid=10, item="GM", maxn=1)
        GM_sun = GM_sun[0]

        # Orbital elements of Ceres
        _orbit_planet_elements = spiceypy.oscltx(
            _planet_state_vector, self._et_time, GM_sun
        )

        self.orbit_semi_major_au = spiceypy.convrt(
            _orbit_planet_elements[9], inunit="km", outunit="AU"
        )
        self.orbit_perihelion_au = spiceypy.convrt(
            _orbit_planet_elements[0], inunit="km", outunit="AU"
        )
        self.orbit_ecentricity = _orbit_planet_elements[1]

        # Create readable (in degrees) representation of angular values
        self.orbit_inclination_deg = np.degrees(_orbit_planet_elements[2])
        self.orbit_longitude_asc_node_deg = np.degrees(_orbit_planet_elements[3])
        self.orbit_arg_perihelion_deg = np.degrees(_orbit_planet_elements[4])

        # Ceres orbital period
        self.orbit_period_years = _orbit_planet_elements[10] / (86400 * 365)

    def show_params(self) -> dict:
        """
        Create a dictionary with orbit parameters

        Returns:
        --------
        dict
            Dictionary containing the following orbit parameters:
            - semi_major_au: Semi-major axis in astronomical units (AU).
            - perihelion_au: Perihelion distance in astronomical units (AU).
            - ecentricity: Orbital eccentricity.
            - inclination_deg: Orbital inclination in degrees.
            - longitude_asc_node_deg: Longitude of the ascending node in degrees.
            - arg_perihelion_deg: Argument of perihelion in degrees.
            - orbital_period_years: Orbital period in years.
        """
        return {
            "semi_major_au": self.orbit_semi_major_au,
            "perihelion_au": self.orbit_perihelion_au,
            "ecentricity": self.orbit_ecentricity,
            "inclination_deg": self.orbit_inclination_deg,
            "longitude_ascendation_node_deg": self.orbit_longitude_asc_node_deg,
            "argument_perihelion_deg": self.orbit_arg_perihelion_deg,
            "orbital_period_years": self.orbit_period_years,
        }
