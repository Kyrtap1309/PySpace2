import numpy as np
import spiceypy
from matplotlib import pyplot as plt

from .solar_system import SolarSystem
from ..utilities.utilities import prepare_dict, show_or_save_fig
from ..utilities.constants import NAIF_PLANETS_ID


class PhaseAngle(SolarSystem):
    def __init__(self, delta_days: int, date: dict, chosen_planets: list) -> None:
        """
        Expand SolarSystem init with phase angles data of different planets

        Parameters:
        -----------
        delta_days : int
            Number of days to compute the trajectory for.
        date : dict
            Starting date for the computation (year, month, day, hour, minute, second).
        chosen_planets: list
            List of planets, which plots are supposed to be generated
        """
        super().__init__(delta_days, date)

        self._add_planets_to_df(chosen_planets)

    def plot(
        self,
        save_fig: bool = True,
        dpi: str = 500,
        fig_name: str = "phase_angle_plot.png",
        dir: str = "./plots",
    ) -> None:
        """
        Plot phase angel of planets with sun based on time

        Parameters:
        -----------
        save_fig: bool
            If plot is supposed to be saved instead of showed
        dpi: int
            dpi of saved plot
        fig_name: str
            name of plot
        dir: str
            relative (to pwd) path of dir with plots
        """

        plt.style.use("dark_background")

        fig, axs = plt.subplots(
            nrows=len(self._naif_chosen_planets.keys()),
            ncols=1,
            sharex=True,
            figsize=(8, 20),
        )

        for ax, planet_name in zip(list(axs), self._naif_chosen_planets.keys()):
            ax.set_title(planet_name, color="orange")

            ax.plot(
                self._solar_system_data_frame["UTC"],
                self._solar_system_data_frame["Barycentre_distance"],
                color="white",
            )

            ax.set_ylabel(
                "Bar. distance in Sun Radius", rotation=90, labelpad=25, fontsize=5
            )

            ax.set_xlim(
                min(self._solar_system_data_frame["UTC"]),
                max(self._solar_system_data_frame["UTC"]),
            )
            ax.set_ylim(0, 2)

            ax_copy = ax.twinx()
            ax_copy.plot(
                self._solar_system_data_frame["UTC"],
                self._solar_system_data_frame[f"{planet_name}_phase_ang"],
                color="orange",
            )

            ax_copy.invert_yaxis()
            ax_copy.set_ylim(180, 0)

            ax_copy.set_ylabel(
                "Phase angel of planet in degrees",
                rotation=90,
                labelpad=25,
                fontsize=5,
                color="orange",
            )

            ax.set_facecolor("navy")
            ax_copy.set_facecolor("navy")

            fig.set_facecolor("#1E2A4C")

            ax.grid(True, linewidth=0.5, linestyle="dashed", alpha=0.7)

            plt.subplots_adjust(hspace=15)

        axs[len(self._naif_chosen_planets.keys()) - 1].set_xlabel("Date")
        fig.tight_layout(pad=5.0)

        show_or_save_fig(dir=dir, fig_name=fig_name, save_fig=save_fig, dpi=dpi)

    def _add_planets_to_df(self, chosen_planets: list) -> None:
        """
        Add to data_frame phase_angle data

        Parameters:
        -----------
        chosen_planets: list
            Planets which phase angels are supposed to be included

        """
        self._naif_chosen_planets = prepare_dict(NAIF_PLANETS_ID, chosen_planets)

        for planets_name in self._naif_chosen_planets.keys():
            planet_pos = f"{planets_name}_pos"
            planet_angle = f"{planets_name}_phase_ang"

            planet_id = self._naif_chosen_planets[planets_name]

            self._solar_system_data_frame.loc[
                :, planet_pos
            ] = self._solar_system_data_frame["ET"].apply(
                lambda x: spiceypy.spkgps(
                    targ=planet_id, et=x, ref="ECLIPJ2000", obs=NAIF_PLANETS_ID["Sun"]
                )[0]
            )
            self._solar_system_data_frame.loc[:, planet_angle] = (
                self._solar_system_data_frame.apply(
                    lambda x: np.degrees(
                        spiceypy.vsep(x[planet_pos], x["barycentre_pos"])
                    ),
                    axis=1,
                )
            )


if __name__ == "__main__":
    chosen_planets = ["Mars", "Jupiter", "Saturn", "Uran"]
    date = {"year": 2001, "month": 9, "day": 13, "hour": 5, "minute": 0, "second": 0}
    phase_angel = PhaseAngle(date=date, delta_days=5000, chosen_planets=chosen_planets)
    phase_angel.plot()
