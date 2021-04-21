from setuptools import setup, find_packages

setup(
    name="dvcchecker",
    packages=find_packages(),
    install_requires=["PyYAML>=5.4"],
    entry_points={"console_scripts": ["dvcchecker = dvcchecker.main:main"]},
)
