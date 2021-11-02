from setuptools import setup

setup(
    name="pruebaMeli",
    version="1.0",
    author='Federico Palumbo',
    py_modules=['nmigen_cocotb'], #
    setup_requires=['pydrive', 'mysql-connector', 'python-dotenv', 'pytest', 'virtualenv'], #virtualenv?
    install_requires=[]
)