import os
import inspect

def get_furnsh_kernel_path(kernel_path):
    """
    Function to obtain the full path to a kernel file based on the project's location.

    Args:
        kernel_path (str): The relative path from the project directory to the kernel file.

    Returns:
        str: The full path to the kernel file.
    """
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    dir = os.path.dirname(os.path.abspath(caller_file))
    furnsh_kernel_path = os.path.join(dir, kernel_path)
    return furnsh_kernel_path