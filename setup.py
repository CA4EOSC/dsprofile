from setuptools import (
    find_packages,
    setup
)


dev_requires = [
    "flake8",
    "pdbpp",
    "pytest"
]

test_requires = [
    "pytest",
    "pytest-cov"
]


setup(
    name = "dsprofile",
    version = "0.2.0",
    packages = find_packages(include=["dsprofile", "dsprofile.*"]),
    install_requires = [
        "setuptools==68.1.2",  # earthpy uses pkg_resources
        "netCDF4",
        "earthpy",             # Includes GeoPandas, rasterio
        "fiona",               # ESRI Shapefile support
        "pyproj",              # CRS parsing
        "python-dotenv"
    ],
    extras_require = {
        "dev": dev_requires,
        "test": test_requires
    },
    entry_points = {
        "console_scripts": ["dsprofile=dsprofile.main:main"]
    }
)
