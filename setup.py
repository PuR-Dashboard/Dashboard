from setuptools import setup, find_packages

def get_requirements():
    """
    Reads the requirements.txt file and returns a list of requirements. Those requirements are then used in the setup.py
    :return:  List of requirements
    """
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements


"""
To install the package, run the following command in the terminal: `python setup.py install`
"""
setup(
    name='Dashboard',
    version='1.0',
    packages=find_packages(),
    author='timmaster',
    description='Package for the use of the Park and Ride Dashboard',
    install_requires=get_requirements()
)
