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
    install_requires=("typeguard"),
    tests_require=("pytest"),
    packages=find_packages(),
)
