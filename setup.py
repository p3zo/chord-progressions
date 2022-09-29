from setuptools import find_packages, setup

__version__ = "0.29.0"

dev_requires = ["black", "flake8", "ipdb", "ipython", "isort", "bumpversion"]

test_requires = ["pytest", "pytest-cov"]

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
        "matplotlib==3.5.1",
        "mido==1.2.10",
        "networkx==2.8",
        "numpy==1.22.3",
        "pandas==1.4.2",
        "pretty_midi==0.2.9",
        "scipy==1.8.0",
    ],
    extras_require={
        "test": test_requires,
        "dev": test_requires + dev_requires,
    },
)
