import spiceypy
import math
from ..utilities.utilities import kernels_load
from ..utilities.constants import AU_TO_KM, ET_TODAY_DATE_MIDNIGHT, NAIF_PLANETS_ID


class Earth:
    def __init__(self):

        kernels = ["../../kernels/spk/de432s.bsp", "../../kernels/pck/gm_de431.tpc"]

        try:
            kernels_load(kernels)
        except Exception as e:
            print(f"Błąd podczas ładowania kerneli: {e}")
            raise

        # Calculating an earth state vector and time of light's travel between
        # the earth and the sun
        # Using spkgeo function with parametres:
        # targ = 399 - NAIF ID of the planet (The Earth in this case) that state vector is pointing
        # et = et_todat - Reference time of calculations
        # ref = 'ECLIPJ2000' - An Ecliptic Plane used in calculations
        # obs = 10 - NAIF ID of the object (The Sun in this case) which is the beggining of state vector

        self.earth_state_vector, self.earth_sun_light_time = spiceypy.spkgeo(
            targ=NAIF_PLANETS_ID["Earth"],
            et=ET_TODAY_DATE_MIDNIGHT,
            ref="ECLIPJ2000",
            obs=NAIF_PLANETS_ID["Sun"],
        )

        # Calculate earth - sun distance (km)
        self.earth_sun_distace = math.sqrt(
            self.earth_state_vector[0] ** 2
            + self.earth_state_vector[1] ** 2
            + self.earth_state_vector[2] ** 2
        )
        # Convert a distance to AU
        self.au_earth_sun_distance = self.earth_sun_distace / AU_TO_KM

        # Calculate the orbital speed of the Earth around the Sun (km/s)
        self.earth_sun_speed = math.sqrt(
            self.earth_state_vector[3] ** 2
            + self.earth_state_vector[4] ** 2
            + self.earth_state_vector[5] ** 2
        )

        # Calculate theorical orbital speed of the Earth around the Sun (km/s)
        _, gm_sun = spiceypy.bodvcd(
            bodyid=NAIF_PLANETS_ID["Sun"], item="GM", maxn=1
        )  # GM parameter
        self.earth_sun_speed_theory = math.sqrt(gm_sun[0] / self.earth_sun_distace)

    def __str__(self):
        info = f"""\n\tEarth location in relation to Sun for {ET_TODAY_DATE_MIDNIGHT}: {self.earth_state_vector} km\n
        Earth distance from Sum equals for {ET_TODAY_DATE_MIDNIGHT}: {self.au_earth_sun_distance} AU\n
        The Earth orbital speed around the Sun equals for: {self.earth_sun_speed}" km/s\n
        The theoretical Earth orbital speed around the Sun equals for: {self.earth_sun_speed_theory} km/s)\n"""
        return info


if __name__ == "__main__":
    earth = Earth()
    print(earth)
