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
    name = "ncmetadata",
    version = "0.1.0",
    packages = find_packages(include=["ncmetadata", "ncmetadata.*"]),
    install_requires = [
        "netCDF4"
    ],
    extras_require = {
        "dev": dev_requires,
        "test": test_requires
    },
    entry_points = {
        "console_scripts": ["ncmetadata=ncmetadata.main:main"]
    }
)
