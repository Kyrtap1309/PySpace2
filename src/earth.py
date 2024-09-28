import spiceypy
import math
from utilities.utilities import get_furnsh_kernel_path

spiceypy.furnsh(get_furnsh_kernel_path('../kernels/spk/de432s.bsp'))