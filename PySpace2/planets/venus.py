import numpy as np
import pandas as pd
import matplotlib.dates
from matplotlib import pyplot as plt
import spiceypy

from ..utilities.utilities import kernels_load, get_utc_time, show_or_save_fig
from ..utilities.constants import HOUR_TO_SECONDS, NAIF_PLANETS_ID


class Venus:
    def __init__(self, begin_date, end_date) -> None:

        # spicepy needs a kernels loaded to work properly
        kernels = [
            "../kernels/spk/de432s.bsp",
            "../kernels/lsk/naif0012.tls",
            "../kernels/pck/pck00010.tpc",
        ]
        kernels_load(kernels)

        self._venus_init(begin_date, end_date)

    def __str__(self):
        """Quick info about computed hours and hours when we can take a photo"""
        info1 = (
            f"Number of hours computed: {len(self._planets_dataframe)}"
            + f" (around {round(len(self._planets_dataframe) / 24)} days)"
        )
        info2 = (
            f"""Number of hours when we can take a photo: {len(self._planets_dataframe.loc
                                                   [self._planets_dataframe['photo-able'] == 1])}"""
            + f" (around {round(len(self._planets_dataframe.loc[self._planets_dataframe['photo-able'] == 1]) / 24)} days)"
        )

        return info1 + "\n" + info2

    def plot(
        self,
        save_fig: bool = True,
        dpi: str = 500,
        fig_name: str = "venus_plot.png",
        dir: str = "./plots",
    ) -> None:
        plt.style.use("dark_background")

        fig, ax = plt.subplots(figsize=(12, 8))

        # plotting angles in function of time
        ax.plot(
            self._planets_dataframe["UTCs"],
            self._planets_dataframe["Earth_Venus_Sun_Angle"],
            color="yellow",
            label="Sun and Venus Angle",
        )

        ax.plot(
            self._planets_dataframe["UTCs"],
            self._planets_dataframe["Earth_Moon_Sun_Angle"],
            color="blue",
            label="Sun and Moon Angle",
        )

        ax.plot(
            self._planets_dataframe["UTCs"],
            self._planets_dataframe["Earth_Venus_Moon_Angle"],
            color="silver",
            label="Venus and Moon Angle",
        )

        ax.set_facecolor("navy")

        ax.set_xlabel("Dates")
        ax.set_ylabel("Angles")

        fig.set_facecolor("#1E2A4C")

        ax.grid(True, linewidth=0.5, linestyle="dashed", alpha=0.7)

        ax.set_xlim(
            min(self._planets_dataframe["UTCs"]), max(self._planets_dataframe["UTCs"])
        )
        ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        ax.xaxis.set_minor_locator(matplotlib.dates.DayLocator())

        ax.legend(fancybox=True, loc="upper right", framealpha=1)

        for photogenic_date in self._planets_dataframe.loc[
            self._planets_dataframe["photo-able"] == 1
        ]["UTCs"]:
            ax.axvline(photogenic_date, color="green", alpha=0.1)

        # Add note about vertical lines meaning in legend
        plt.plot([], [], " ", label="Vertical lines -- photographable days")
        plt.legend()

        plt.xticks(rotation=45)
        show_or_save_fig(dir=dir, fig_name=fig_name, save_fig=save_fig, dpi=dpi)

    def _venus_init(self, begin_date, end_date) -> None:

        self._init_utc_time = get_utc_time(begin_date)
        self._end_utc_time = get_utc_time(end_date)

        # Initialization of UTC time
        self._init_time_utc_str = self._init_utc_time.strftime("%Y-%m-%dT%H:%M:%S")
        self._end_time_utc_str = self._end_utc_time.strftime("%Y-%m-%dT%H:%M:%S")

        # Ephemeris time
        _init_et_time = spiceypy.utc2et(self._init_time_utc_str)
        _end_et_time = spiceypy.utc2et(self._end_time_utc_str)

        # Time interval in seconds is pause in calculating next
        # phase angel
        _time_interval = np.arange(_init_et_time, _end_et_time, HOUR_TO_SECONDS)

        # Creating a pandas dataframe to store calculations and parameters
        self._planets_dataframe = pd.DataFrame()

        # Column with ET times
        self._planets_dataframe.loc[:, "ETs"] = _time_interval

        # column with Utc times
        self._planets_dataframe.loc[:, "UTCs"] = self._planets_dataframe["ETs"].apply(
            lambda x: spiceypy.et2datetime(et=x)
        )
        # Compute an angle between Venus and Sun when we measure it from Earth
        self._planets_dataframe.loc[
            :, "Earth_Venus_Sun_Angle"
        ] = self._planets_dataframe["ETs"].apply(
            lambda x: np.degrees(
                spiceypy.phaseq(
                    et=x,
                    target=str(NAIF_PLANETS_ID["Earth"]),  # earth NAIF id
                    illmn=str(NAIF_PLANETS_ID["Sun"]),  # sun NAIF ID
                    obsrvr=str(NAIF_PLANETS_ID["Venus"]),  # venus NAIF id
                    abcorr="LT+S",  # Correction because of
                    # finite light speed
                )
            )
        )
        # Compute an angle between the Venus and the Moon when we measure it from Earth
        self._planets_dataframe.loc[
            :, "Earth_Venus_Moon_Angle"
        ] = self._planets_dataframe["ETs"].apply(
            lambda x: np.degrees(
                spiceypy.phaseq(
                    et=x,
                    target=str(NAIF_PLANETS_ID["Earth"]),  # earth NAIF id
                    illmn=str(NAIF_PLANETS_ID["Venus"]),  # venus NAIF ID
                    obsrvr=str(NAIF_PLANETS_ID["Moon"]),  # moon NAIF id
                    abcorr="LT+S",  # Correction because of
                    # finite light speed
                )
            )
        )
        self._planets_dataframe.loc[
            :, "Earth_Moon_Sun_Angle"
        ] = self._planets_dataframe["ETs"].apply(
            lambda x: np.degrees(
                spiceypy.phaseq(
                    et=x,
                    target=str(NAIF_PLANETS_ID["Earth"]),  # earth NAIF id
                    illmn=str(NAIF_PLANETS_ID["Sun"]),  # sun NAIF ID
                    obsrvr=str(NAIF_PLANETS_ID["Moon"]),  # moon NAIF id
                    abcorr="LT+S",  # Correction because of
                    # finite light speed
                )
            )
        )
        # Now is needed to make a column which inform us when we can take a photo of
        # a constelation of Venus, Mars and Sun. It is possible when:
        # Moon -- Venus angle < 10 degrees
        # Moon -- Sun angle > 30 degrees
        # Venus -- Sun angle > 30 degrees
        self._planets_dataframe.loc[:, "photo-able"] = self._planets_dataframe.apply(
            lambda x: (
                1
                if (x["Earth_Venus_Moon_Angle"] < 10.0)
                and (x["Earth_Moon_Sun_Angle"] > 30.0)
                and (x["Earth_Venus_Sun_Angle"] > 30.0)
                else 0
            ),
            axis=1,
        )


if __name__ == "__main__":
    begin_date = {
        "year": 2001,
        "month": 9,
        "day": 13,
        "hour": 5,
        "minute": 0,
        "second": 0,
    }
    end_date = {
        "year": 2001,
        "month": 10,
        "day": 8,
        "hour": 3,
        "minute": 0,
        "second": 0,
    }
    venus = Venus(begin_date, end_date)
    print(venus)
    venus.plot()
