#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from setuptools import setup, find_packages
from mesonui.packageinfo import PackageInfo as PyPiPackage

try:
    pypi_pkg: PyPiPackage = PyPiPackage()
except Exception as e:
    print(f"Error: Failed to retrieve package information - {e}")
    raise

setup(
    author=pypi_pkg.get_name(),
    author_email=pypi_pkg.get_mail(),
    name=pypi_pkg.get_project_name(),
    description=pypi_pkg.get_description(),
    long_description=pypi_pkg.long_description(),
    version=pypi_pkg.get_version(),
    license=pypi_pkg.get_license(),
    packages=find_packages(),
    entry_points={
        'console_scripts': ['meson-ui=mesonui.mesonuimain:mesonui_main'],
    },
    install_requires=['meson', 'ninja', 'PyQt5'],
    setup_requires=['pytest-runner'],
    zip_safe=True,
    include_package_data=True
)
