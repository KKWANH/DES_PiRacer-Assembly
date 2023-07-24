# Copyright (C) 2022 twyleg
import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='piracer_py',
    version=read('VERSION.txt'),
    author='Torsten Wylegala',
    author_email='mail@twyleg.de',
    description='Simple abstraction layer for PiRacer and PiRacer Pro',
    license='GPL 3.0',
    keywords='piracer embedded abstraction',
    url='https://github.com/twyleg/piracer_py',
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        'wheel',
        'RPi.GPIO',
        'adafruit-circuitpython-pca9685',
        'adafruit-circuitpython-ina219',
        'adafruit-circuitpython-ssd1306',
        'opencv-python'
    ],
    entry_points={}
)