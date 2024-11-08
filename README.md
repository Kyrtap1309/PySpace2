# PySpace2

## Description

**PySpace2** is a Python library that allows for advanced astronomical calculations, simulations, and data analysis related to outer space. The project aims to simplify operations on celestial bodies, their movements, and the dynamics of planetary systems.

## Features

- Calculating the real and theorical Earth speed
- Plotting the Solar System Barycentre with relation to Sun
- Analyze when you can take photo of Venus
- Create Planets' map with Equator Coordinates System 

## System Requirements

- Python 3.9+
- Supported operating systems: Windows, macOS, Linux

---

## Installation

To install the **PySpace2** package, use the `pip` package manager:

```bash
pip install PySpace2
```
If you are installing the package from the repository, ensure you have the latest version of pip, and then install it locally:

```bash
git clone git@github.com:your-account/pyspace2.git
cd pyspace2
pip install .
```

## Examples
Check package usage examples [here](docs/examples)

## Documentation Website
PySpace2 uses MkDocs to generate documentation. If you want to generate it locally, follow these steps:

1. Move to the root directory of the PySpace2 project where the **requirements** folder is located: 

2. Install MkDocs and required plugins

```bash
pip install -r requirements/docs.txt
```

3. Serve the documentation locally

    

```bash
mkdocs serve
```
This will start a local server, and the documentation can be viewed in your browser at http://127.0.0.1:8000.

4. Build the documentation (optional)

If you want to generate a static HTML version of the documentation, you can run:

```bash
mkdocs build
```

This will create a **site/** directory with all the HTML files needed to host the documentation.

## Gallery

### Example: Solar System Barycentre trajectory with First Kepler functionality
![First Kepler](docs/static/img/barycentre_trajectory.png)

### Example: Plot a graph of phase angle of planets based on time
![Phase Angle](docs/static/img/phase_angle_plot.png)

### Example: Planets' Map at Equatorial Coordinate System
![Map](docs/static/img/space_map.png)