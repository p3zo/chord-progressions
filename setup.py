from setuptools import find_packages, setup

__build__ = 0
__version__ = f"0.0.1.{__build__}"


setup(
    name="chord-progressions",
    author="p3zo",
    version=__version__,
    packages=find_packages(
        exclude=[
            "tests",
            "tests.*",
        ]
    ),
    package_data={},
    python_requires=">=3.6",
)
