import os
import inspect
import spiceypy
import pathlib
import platform
import requests

from functools import wraps

def kernels_load(kernels_path: list[str]) -> None:
    """
    Function to load many kernels at once.

    Args:
        kernels_path (list[str]): List of relative paths
    """
    for kernel_path in kernels_path:
        spiceypy.furnsh(_get_furnsh_kernel_path(kernel_path))


def create_folder_if_not_exists(folder_path: str) -> None:
    """
    Function to create dir if it does not exist.

    Args:
        folder_path (str): The relative path
    """
    folder = pathlib.Path(folder_path)
    if not folder.exists():
        folder.mkdir(parents=True)



def show_or_save_fig(
    dir: str = "./plots",
    fig_name: str = "plot.png",
    save_fig: bool = True,
    dpi: int = 400,
):
    """
    Function to handle saving or showing generated plot

    Args:
        dir (str): The relative path (relative to cwd) of figure (if saved)
        fig_name (str): Name of plot file
        save_fig (bool): If True, save plot as picture, else show as interactive
        dpi (int): dpi of plot picture

    """

    from matplotlib import pyplot as plt

    if save_fig:
        create_folder_if_not_exists(dir)
        plt.savefig(os.path.join(dir, fig_name), dpi=dpi)
    else:
        try:
            plt.show()
        except Exception as e:
            print(
                f"Error during displaying trajectory: {e}, trajectory saved as {fig_name}"
            )
            create_folder_if_not_exists(dir)
            plt.savefig(os.path.join(dir, fig_name), dpi=dpi)


def prepare_dict(original_dict: dict, keys_list: list):
    """
    Create a needed sample of dict

    Args:
        original_dict(dict):
        keys_of_list(list):
    """

    return {key: original_dict[key] for key in keys_list if key in original_dict}


def get_utc_time(date_dict: dict):
    import datetime

    utc_date = datetime.datetime(
        year=date_dict["year"],
        month=date_dict["month"],
        day=date_dict["day"],
        hour=date_dict["hour"],
        minute=date_dict["minute"],
        second=date_dict["second"],
    )

    return utc_date

def _get_furnsh_kernel_path(kernel_path: str) -> str:
    """
    Function to obtain the full path to a kernel file based on the project's location.

    Args:
        kernel_path (str): The relative path.

    Returns:
        str: The full path to the kernel file.
    """
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    dir = os.path.dirname(os.path.abspath(caller_file))
    furnsh_kernel_path = os.path.join(dir, kernel_path)

    current_os = platform.system()

    if current_os == "Windows":
        furnsh_kernel_path = furnsh_kernel_path.replace("/", "\\")

    return furnsh_kernel_path
