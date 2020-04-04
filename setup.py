import os
from setuptools import setup, find_packages

#import pdb; pdb.set_trace()

# Utility function to read the README file.
setup(
    description = ("A new website for AEIR association."),
    license = "MIT",
    keywords = "AEIR INSA Rennes",
    packages = find_packages(),
    include_package_data = True,
)