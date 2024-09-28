import os

def get_furnsh_kernel_path(kernel_path):
    """
    Function to obtain the full path to a kernel file based on the project's location.

    Args:
        kernel_path (str): The relative path from the project directory to the kernel file.

    Returns:
        str: The full path to the kernel file.
    """
    module_path = os.path.dirname(os.path.abspath(__file__))
    furnsh_kernel_path = os.path.join(module_path, kernel_path)
    return furnsh_kernel_path