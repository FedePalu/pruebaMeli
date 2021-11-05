from setuptools import find_packages, setup

setup(
    name="pruebaMeli",
    version="1.0",
    author='Federico Palumbo',
    install_requires=['pydrive', 'mysql-connector', 'pytest'],
    package = find_packages('.')
)