KERNELS_URLS = {
    "lsk/naif0012.tls": "generic_kernels/lsk/naif0012.tls",
    "pck/gm_de431.tpc": "generic_kernels/pck/gm_de431.tpc",
    "pck/pck00010.tpc": "generic_kernels/pck/pck00010.tpc",
    "spk/de432s.bsp": "generic_kernels/spk/planets/de432s.bsp",
    "general/codes_300ast_20100725.bsp": "generic_kernels/spk/asteroids/codes_300ast_20100725.bsp",
    "general/codes_300ast_20100725.tf": "generic_kernels/spk/asteroids/codes_300ast_20100725.tf",
}


REQUIRED_FILES = {
    "earth": ["spk/de432s.bsp", "pck/gm_de431.tpc"],
    "first_kepler": ["spk/de432s.bsp", "pck/pck00010.tpc"],
    "solar_system": ["spk/de432s.bsp", "pck/pck00010.tpc"],
    "phase_angel": ["spk/de432s.bsp", "pck/pck00010.tpc"],
    "venus": [
        "spk/de432s.bsp",
        "lsk/naif0012.tls",
        "pck/pck00010.tpc",
    ],
    "map": ["spk/de432s.bsp", "lsk/naif0012.tls"],
    "orbit": [
        "spk/de432s.bsp",
        "lsk/naif0012.tls",
        "pck/gm_de431.tpc",
        "general/codes_300ast_20100725.bsp",
        "general/codes_300ast_20100725.tf",
    ],
}
