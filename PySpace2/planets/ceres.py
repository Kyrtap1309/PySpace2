from ..utilities.kernels_constants import REQUIRED_FILES
from ..utilities.kernels_utilities import kernels_load

class Ceres:
    def __init__(self) -> None:
        self._kernels_load()
        self._ceres_init()


    def _kernels_load(self) -> None:
        """
        Function to load kernels
        """
        kernels = REQUIRED_FILES[self.__class__.__name__.lower()]
        kernels_load(kernels)

    def _ceres_init(self) -> None:
        pass