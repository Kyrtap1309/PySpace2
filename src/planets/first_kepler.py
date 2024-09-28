import datetime
import numpy as np
import spiceypy
import matplotlib
from matplotlib import pyplot as plt

from ..utilities.utilities import kernels_load
from ..utilities.constants import NAIF_PLANETS_ID


class FirstKepler:

    def __init__(self, delta_days: int, date: dict) -> None:
        # spicepy needs a kernels loaded to work properly
        kernels = ["../../kernels/spk/de432s.bsp", "../../kernels/pck/pck00010.tpc"]
        kernels_load(kernels)

        self.init_time = datetime.datetime(
            year=date["year"],
            month=date["month"],
            day=date["day"],
            hour=date["hour"],
            minute=date["minute"],
            second=date["second"],
        )

        self.end_time = self.init_time + datetime.timedelta(days=delta_days)

        # Initialization of UTC time
        init_time_utc_str = self.init_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time_utc_str = self.end_time.strftime("%Y-%m-%dT%H:%M:%S")

        # Ephemeris time
        init_et_time = spiceypy.utc2et(init_time_utc_str)
        end_et_time = spiceypy.utc2et(end_time_utc_str)

        # Create numpy array with one day interval between start and end day
        time_array = np.linspace(init_et_time, end_et_time, delta_days)

        # Array with all positions of solar system barycentre
        solar_system_barycentre_pos = []

        for time in time_array:
            _position, _ = spiceypy.spkgps(
                targ=NAIF_PLANETS_ID["SSB"],
                et=time,
                ref="ECLIPJ2000",
                obs=NAIF_PLANETS_ID["Sun"],
            )
            solar_system_barycentre_pos.append(_position)

        # convert to numpy array
        self.solar_system_barycentre_pos_array = np.array(solar_system_barycentre_pos)

        # import sun radius
        _, sun_radius_arr = spiceypy.bodvcd(
            bodyid=NAIF_PLANETS_ID["Sun"], item="RADII", maxn=3
        )
        self.sun_radius = sun_radius_arr[0]

        # Scalled solar system barycentre position (in Sun radii)
        self.solar_system_barycentre_pos_scalled = (
            self.solar_system_barycentre_pos_array / self.sun_radius
        )

    def __str__(self) -> str:
        # Print the starting and end times
        info = f"""\tStart day: {self.init_utc_time_str}
        End day: {self.end_utc_time_str}"""
        return info

    def trajectory(self, save_fig:bool = True, dpi:str =500, fig_name:str = "barycentre_trajectory.png") -> None:
        # Plotting trajectory of solar system barycentre (only needed x and y coordinates)
        solar_system_barycentre_pos_scalled_plane = (
            self.solar_system_barycentre_pos_scalled[:, 0:2]
        )


        plt.style.use("dark_background")

        fig, ax = plt.subplots(figsize=(12, 8))

        # Create a yellow circle that represents the Sun, add it to the ax
        sun = plt.Circle((0.0, 0.0), 1.0, color="yellow", alpha=0.8)
        ax.add_artist(sun)

        ax.plot(
            solar_system_barycentre_pos_scalled_plane[:, 0],
            solar_system_barycentre_pos_scalled_plane[:, 1],
            ls="solid",
            color="royalblue",
        )

        ax.set_aspect('equal')
        ax.grid(True, linestyle='dashed', alpha=0.5)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)

        ax.set_xlabel('X in Sun-Radius')
        ax.set_ylabel('Y in Sun-Radius')

        if save_fig:
            plt.savefig(fig_name, dpi = dpi)
        else:
            try:
                plt.show()
            except Exception as e:
                print(f"Error during displaying trajectory: {e}, trajectory saved as {fig_name}")
                plt.savefig(fig_name, dpi=dpi)

if __name__ == "__main__":
    date = { "year": 2001,
            "month": 9,
            "day": 13,
            "hour": 5,
            "minute": 0,
            "second": 0
    }
    first_kepler = FirstKepler(date=date, delta_days=5000)
    first_kepler.trajectory()