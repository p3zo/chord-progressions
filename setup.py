import os

from setuptools import find_packages, setup

__version__ = "0.8.0"

dev_requires = ["black", "flake8", "ipdb", "ipython", "isort", "bumpversion"]

test_requires = ["pytest", "pytest-cov"]

# dependencies for features not yet fully integrated into the core API
experimental_requires = [
    "joblib==0.17.0",
    "matplotlib==3.3.3",
    "networkx==2.5",
    "pandas==1.2.4",
    "psutil==5.8.0",
    "tables==3.6.1",
    "torch==1.6.0",
    "torchvision==0.8.0",
    "tqdm==4.51.0",
]

setup(
    name="chord-progressions",
    author="p3zo",
    version=__version__,
    url="https://github.com/p3zo/chord-progressions",
    packages=find_packages(
        exclude=[
            "tests*",
        ]
    ),
    package_data={},
    python_requires=">=3.6",
    install_requires=[
        "mido==1.2.9",
        "numpy==1.19.4",
        "pretty_midi==0.2.9",
        "scipy==1.6.2",
    ],
    extras_require={
        "test": test_requires,
        "dev": test_requires + dev_requires,
        "experimental": [experimental_requires],
    },
)
