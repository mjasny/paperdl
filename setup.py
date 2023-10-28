#!/usr/bin/env python3


from setuptools import setup

setup(
    name='paperdl',
    version='1.0',
    description='Download papers using constitutional access',
    author='Matthias Jasny',
    author_email='matthias.jasny@cs.tu-darmstadt.de',
    url='',
    packages=[],
    install_requires=[
        'requests[socks]',
        'paramiko @ git+https://github.com/linwownil/paramiko.git@add-socks-proxy',
        'playwright',
    ],
    entry_points={
        'console_scripts': [
            'paperdl = paperdl.paperdl:main'
        ]
    },
)
