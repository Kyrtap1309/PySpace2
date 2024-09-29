import os
import inspect
import spiceypy
import pathlib
import platform


def get_furnsh_kernel_path(kernel_path: str) -> str:
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


def kernels_load(kernels_path: str) -> None:
    """
    Function to load many kernels at once.

    Args:
        kernels_path (list[str]): List of relative paths
    """

    for kernel_path in kernels_path:
        spiceypy.furnsh(get_furnsh_kernel_path(kernel_path))


def create_folder_if_not_exists(folder_path: str) -> None:
    """
    Function to create dir if it does not exist.

    Args:
        folder_path (str): The relative path
    """
    folder = pathlib.Path(folder_path)
    if not folder.exists():
        folder.mkdir(parents=True)

def show_or_save_fig(dir, fig_name, save_fig, dpi):
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