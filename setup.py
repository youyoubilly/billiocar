from setuptools import setup, find_packages

setup(
    name='bcar', 
    version='1.0.0', 
    packages=find_packages(),
    author='Billy Wang, Kevin Peng, Shawn Ling',
    install_requires=[
        'setuptools',
        'adafruit-blinka',
        'adafruit-circuitpython-PCA9685',
        'adafruit-circuitpython-motor',
        'adafruit-circuitpython-motorkit',
                    ],
)