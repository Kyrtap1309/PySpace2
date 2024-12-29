import sqlite3

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from ..utilities.utilities import get_furnsh_path, show_or_save_fig


class Comets:
    def __init__(self) -> None:
        """
        Initialize the Comets class with the database connection
        """
        _sql_path = get_furnsh_path("../database/comets.db")

        #Connect to the comets database
        _conn = sqlite3.connect(_sql_path)
        

        #Create dataframes with P and C type comets
        #Explanation of comets' types: https://en.wikipedia.org/wiki/List_of_comets_by_type
        self.p_type_def = pd.read_sql(
            'SELECT APHELION_AU, INCLINATION_DEG FROM comets_main WHERE ORBIT_TYPE="P"',
            _conn,
        )
        self.c_type_def = pd.read_sql(
            'SELECT APHELION_AU, INCLINATION_DEG FROM comets_main WHERE ORBIT_TYPE="C"',
            _conn,
        )

    def description(self, type: str) -> str:
        """
        Return the statistics of chosen type of comets

        Parameters:
        -----------
        type : str
            Type of comets 

        Return:
        -------
        description : str
            Statistcs of chosen type of comets
        """
        comet_dataframes = {"P": self.p_type_def, "C": self.c_type_def}
        chosen_dataframe = comet_dataframes[type]

        if type == "P":
            description = f"""
            Statistics of P type comets:
            {self.p_type_def.describe()} \n
            """
        elif type == "C":
            description = f"""
            Statistics of C type comets with an eccentricity (bound) < 1:
            {self.c_type_def.loc[self.c_type_def["ECCENTRICITY"]<1].describe()} \n

            Statistics of C type comets with an eccentricity (unbound) >= 1:
            {self.c_type_def.loc[self.c_type_def["ECCENTRICITY"]>=1].describe()} \n
            """

        return description
    
    def plot_inc_vs_aph(
        self,
        save_fig: bool = True,
        dpi: str = 500,
        fig_name: str = "Comet_plot_inc_aph.png",
        dir: str = "./plots",
    ) -> None:
        """
        Plots the inclination vs aphelion of comets with bound orbits

        """

        plt.style.use("dark_background")
        plt.rcParams.update({"font.size": 14})

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(self.p_type_def["APHELION_AU"], 
                   self.p_type_def["INCLINATION_DEG"], 
                   color="tab:orange", 
                   marker='.', 
                   label="P type comets",
                   alpha=0.2)
        
        ax.scatter(self.c_type_def.loc[self.c_type_def["ECCENTRICITY"]<1]["APHELION_AU"],
                   self.c_type_def.loc[self.c_type_def["ECCENTRICITY"]<1]["INCLINATION_DEG"],
                   color="tab:blue",
                   marker='o',
                   label="C type comets with bound orbits",
                   alpha=0.7)
        
        ax.set_xscale("log")
        ax.set_ylim(0, 180)

        ax.grid(True, axis="both", linestyle="--", alpha=0.3)

        ax.set_title("Inclination vs Aphelion of comets")
        ax.set_xlabel("Aphelion distance [AU]")
        ax.set_ylabel("Inclination [deg]")

        leg = ax.legend(loc="upper right", bbox_to_anchor=[1.1, 1.1], prop={"size": 10})

        for lh in leg.legendHandles:
            lh.set_alpha(1)

        show_or_save_fig(dir=dir, fig_name=fig_name, save_fig=save_fig, dpi=dpi)
    