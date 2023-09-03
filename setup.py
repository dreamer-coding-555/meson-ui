#!/usr/bin/env python3
#
# file: setup.py
# author: Michael Gene Brockus (Dreamer)
# gmail: <michaelbrockus@gmail.com>
#
from setuptools import setup


if __name__ == '__main__':
    setup(
        name='prog',
        version='0.1.0',
        author='Michael Gene Brockus (Dreamer)',
        author_email='michaelbrockus@gmail.com',
        license='Apache 2.0',
        zip_safe=True,
        url='https://github.com/dreamer-coding-555/pypi_program_py',
        packages=[
            'code'
        ],
        python_requires='>=3.8',
        entry_points={
            'console_scripts': [
                'prog=code.main:main_prog',
            ],
        }
    )
