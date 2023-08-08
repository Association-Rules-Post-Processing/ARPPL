from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="arppl",
    version="0.0.3",
    author="Luiz Cintra",
    author_email="contatoluizfernandodev@gmail.com",
    description="A package for post-processing association rules",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Association-Rules-Post-Processing/ARPPL",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
