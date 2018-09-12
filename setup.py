from setuptools import setup, find_packages

description = """
Neat validation of function arguments using Python's annotation system.
"""

setup(
    name="parachute",
    version="0.1",
    description=description,
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    license="GPL-3.0",
    python_requires=">= 3.7",
    install_requires=("typeguard"),
    tests_require=("pytest"),
    extras_require={"ndarray": ["numpy"]},
    # The package is in a seemingly redundant `src` dir.
    # Reason: https://blog.ionelmc.ro/2014/05/25/python-packaging/
    package_dir={"": "src"},
    packages=find_packages("src"),
)
