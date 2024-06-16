#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
"""A library of random helper functionality."""
from pathlib import Path
import subprocess
import functools
import platform
import operator
import unittest
import shutil
import os
import re

import typing as T


def find_executables(file_names: T.List[str]) -> str:
    for file_name in file_names:
        res = shutil.which(file_name)
        if res is not None:
            return res
    raise RuntimeError(f'Executable(s) "{", ".join(file_names)}" not found in path.')


'''
This is the main exception class for Meson-UI
'''
class MesonUiExceptionType(Exception):
    '''Exceptions thrown by Meson-UI'''

'''
Exception classes for parts of both (Meson-UI, CMeson) apps
'''
class MesonUiException(MesonUiExceptionType):
    '''Exceptions thrown by Meson-UI'''

class CMesonException(MesonUiExceptionType):
    '''Exceptions thrown by CMeson'''

class MesonWrapperException(MesonUiExceptionType):
    '''Exceptions thrown by Meson Wrapper class'''

'''
Exception classes for other things like backends and cache
'''
class BackendException(MesonUiExceptionType):
    '''Exceptions thrown by Backend'''


class OSUtility:
    @staticmethod
    def is_sunos() -> bool:
        return platform.system().lower() == 'sunos'

    @staticmethod
    def is_osx() -> bool:
        return platform.system().lower() == 'darwin'

    @staticmethod
    def is_linux() -> bool:
        return platform.system().lower() == 'linux'

    @staticmethod
    def is_haiku() -> bool:
        return platform.system().lower() == 'haiku'

    @staticmethod
    def is_openbsd() -> bool:
        return platform.system().lower() == 'openbsd'

    @staticmethod
    def is_windows() -> bool:
        platname = platform.system().lower()
        return platname == 'windows' or 'mingw' in platname

    @staticmethod
    def is_cygwin() -> bool:
        return platform.system().lower().startswith('cygwin')

    @staticmethod
    def is_debianlike() -> bool:
        return Path('/etc/debian_version').is_file()

    @staticmethod
    def is_dragonflybsd() -> bool:
        return platform.system().lower() == 'dragonfly'

    @staticmethod
    def is_netbsd() -> bool:
        return platform.system().lower() == 'netbsd'

    @staticmethod
    def is_freebsd() -> bool:
        return platform.system().lower() == 'freebsd'


class CIUtility:
    def is_ci(self):
        if 'CI' in os.environ:
            return True
        return False

    def is_pull(self):
        # Travis
        if os.environ.get('TRAVIS_PULL_REQUEST', 'false') != 'false':
            return True
        # Azure
        if 'SYSTEM_PULLREQUEST_ISFORK' in os.environ:
            return True
        return False

    @staticmethod
    def _git_init():
        #
        # TODO: impl GitUtility and Git wrapper class
        subprocess.Popen(['git', 'init'], stderr=subprocess.PIPE).communicate()[0]
        subprocess.Popen(['git', 'config', 'user.name', 'Author Person'], stderr=subprocess.PIPE).communicate()[0]
        subprocess.Popen(['git', 'config', 'user.email', 'teh_coderz@example.com'], stderr=subprocess.PIPE).communicate()[0]
        subprocess.Popen(['git', 'add', '*'], stderr=subprocess.PIPE).communicate()[0]
        subprocess.Popen(['git', 'commit', '-a', '-m', 'I am a project'], stderr=subprocess.PIPE).communicate()[0]

    def skip_if_no_git(self, f):
        '''
        Skip this test if no git is found, unless we're on CI.
        This allows users to run our test suite without having
        git installed on, f.ex., macOS, while ensuring that our CI does not
        silently skip the test because of misconfiguration.
        '''
        @functools.wraps(f)
        def wrapped(self, *args, **kwargs):
            if not self.is_ci() and shutil.which('git') is None:
                raise unittest.SkipTest('Git not found')
            return f(*args, **kwargs)
        return

# a helper class which implements the same version ordering as RPM
class Version:
    def __init__(self, s):
        self._s = s

        # split into numeric, alphabetic and non-alphanumeric sequences
        sequences = re.finditer(r'(\d+|[a-zA-Z]+|[^a-zA-Z\d]+)', s)
        # non-alphanumeric separators are discarded
        sequences = [m for m in sequences if not re.match(r'[^a-zA-Z\d]+', m.group(1))]
        # numeric sequences are converted from strings to ints
        sequences = [int(m.group(1)) if m.group(1).isdigit() else m.group(1) for m in sequences]

        self._v = sequences

    def __str__(self):
        return f'{self._s} (V={self._v})'

    def __repr__(self):
        return '<Version: {}>'.format(self._s)

    def __lt__(self, other):
        if isinstance(other, Version):
            return self.__cmp(other, operator.lt)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Version):
            return self.__cmp(other, operator.gt)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Version):
            return self.__cmp(other, operator.le)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Version):
            return self.__cmp(other, operator.ge)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Version):
            return self._v == other._v
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Version):
            return self._v != other._v
        return NotImplemented

    def __cmp(self, other, comparator):
        # compare each sequence in order
        for ours, theirs in zip(self._v, other._v):
            # sort a non-digit sequence before a digit sequence
            ours_is_int = isinstance(ours, int)
            theirs_is_int = isinstance(theirs, int)
            if ours_is_int != theirs_is_int:
                return comparator(ours_is_int, theirs_is_int)

            if ours != theirs:
                return comparator(ours, theirs)

        # if equal length, all components have matched, so equal
        # otherwise, the version with a suffix remaining is greater
        return comparator(len(self._v), len(other._v))

def _version_extract_cmpop(vstr2: str) -> T.Tuple[T.Callable[[T.Any, T.Any], bool], str]:
    if vstr2.startswith('>='):
        cmpop = operator.ge
        vstr2 = vstr2[2:]
    elif vstr2.startswith('<='):
        cmpop = operator.le
        vstr2 = vstr2[2:]
    elif vstr2.startswith('!='):
        cmpop = operator.ne
        vstr2 = vstr2[2:]
    elif vstr2.startswith('=='):
        cmpop = operator.eq
        vstr2 = vstr2[2:]
    elif vstr2.startswith('='):
        cmpop = operator.eq
        vstr2 = vstr2[1:]
    elif vstr2.startswith('>'):
        cmpop = operator.gt
        vstr2 = vstr2[1:]
    elif vstr2.startswith('<'):
        cmpop = operator.lt
        vstr2 = vstr2[1:]
    else:
        cmpop = operator.eq

    return (cmpop, vstr2)

def version_compare(vstr1: str, vstr2: str) -> bool:
    (cmpop, vstr2) = _version_extract_cmpop(vstr2)
    return cmpop(Version(vstr1), Version(vstr2))

def version_compare_many(vstr1, conditions):
    if not isinstance(conditions, (list, tuple, frozenset)):
        conditions = [conditions]
    found = []
    not_found = []
    for req in conditions:
        if not version_compare(vstr1, req):
            not_found.append(req)
        else:
            found.append(req)
    return not_found == [], not_found, found

# determine if the minimum version satisfying the condition |condition| exceeds
# the minimum version for a feature |minimum|
def compare_minimum_version(condition: str, minimum: str) -> bool:
    if condition.startswith('>='):
        cmpop = operator.le
        condition = condition[2:]
    elif condition.startswith('<='):
        return False
    elif condition.startswith('!='):
        return False
    elif condition.startswith('=='):
        cmpop = operator.le
        condition = condition[2:]
    elif condition.startswith('='):
        cmpop = operator.le
        condition = condition[1:]
    elif condition.startswith('>'):
        cmpop = operator.lt
        condition = condition[1:]
    elif condition.startswith('<'):
        return False
    else:
        cmpop = operator.le

    # Declaring a project(meson_version: '>=0.46') and then using features in
    # 0.46.0 is valid, because (knowing the meson versioning scheme) '0.46.0' is
    # the lowest version which satisfies the constraint '>=0.46'.
    #
    # But this will fail here, because the minimum version required by the
    # version constraint ('0.46') is strictly less (in our version comparison)
    # than the minimum version needed for the feature ('0.46.0').
    #
    # Map versions in the constraint of the form '0.46' to '0.46.0', to embed
    # this knowledge of the meson versioning scheme.
    condition = condition.strip()
    if re.match(r'^\d+.\d+$', condition):
        condition += '.0'

    return cmpop(Version(minimum), Version(condition))

def default_libdir():
    if OSUtility.is_debianlike():
        try:
            pc = subprocess.check_output(['dpkg-architecture', '-qDEB_HOST_MULTIARCH'],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.DEVNULL)
            (stdo, _) = pc.communicate()
            if pc.returncode == 0:
                archpath = stdo.decode().strip()
                return 'lib/' + archpath
        except Exception:
            pass
    if OSUtility.is_freebsd():
        return 'lib'
    if Path('/usr/lib64').is_dir() and not Path('/usr/lib64').is_symlink():
        return 'lib64'
    return 'lib'

def default_libexecdir():
    # There is no way to auto-detect this, so it must be set at build time
    return 'libexec'

def default_prefix():
    return 'c:/' if OSUtility.is_windows() else '/usr/local'
