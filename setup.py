#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='PhotostreamPy',
    version='1.0.1',
    url='https://github.com/amboxer21/PhotoStreamPy',
    license='GPL-3.0',
    author='Anthony Guevara',
    author_email='amboxer21@gmail.com',
    description="Downloads all of your Facebook photos to your Linux desktop.",
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
    zip_safe=True,
    setup_requires=['wget','selenium'],)
