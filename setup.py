import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "aaeir_website",
    version = "0.0.1",
    author = "Théo Guyard",
    author_email = "guyard.theo@gmail.com",
    description = ("A new website for AEIR association."),
    license = "MIT",
    keywords = "AEIR INSA Rennes",
    long_description=read('README'),
)