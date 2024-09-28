import os
import inspect
import spiceypy


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
    return furnsh_kernel_path


def kernels_load(kernels_path: str) -> None:
    """
    Function to load many kernels at once.

    Args:
        kernels_path (list[str]): List of relative paths
    """

    for kernel_path in kernels_path:
        spiceypy.furnsh(get_furnsh_kernel_path(kernel_path))


