#!/usr/bin/env python
"""
Setup script for the `PyTrinamicMicro` package.
"""

import setuptools

setuptools.setup(
    name='PyTrinamicMicro',
    author='Maxim-Trinamic Software Team',
    author_email='pypi.trinamic@maximintegrated.com',
    description='PyTrinamicMicro package for TMCM-0960-MotionPy python master board.',
    long_description_content_type='text/markdown',
    url='https://github.com/trinamic/PyTrinamicMicro',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
)
