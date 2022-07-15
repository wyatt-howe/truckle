"""
A simple setuptools alternative for packing Python FFI bindings into wheels.
"""
from __future__ import annotations

import base64
import glob
import hashlib
import os
import sys
import zipfile
from typing import Union
import doctest
import toml
from packaging.tags import platform_tags


def truckle(pyproject_path: str, minor_version: Union[str,int] = None, wheel_file_name: str = None) -> str:
    # pylint: disable=C0301 # Accommodates long link URLs.
    """
    Build a wheel.

    Example.

    >>> 1 in [1]
    True
    """

    plattag = next(platform_tags()) or 'py3-none-any'

    project_root = pyproject_path[:-len('pyproject.toml')]

    minor_version = minor_version or sys.version_info.minor

    with open(pyproject_path, 'r') as fd:
        pyproject = toml.loads(fd.read())
        fd.close()

    # {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
    wheel_file_name = wheel_file_name or F"{pyproject['project']['name']}-" \
                                         F"{pyproject['project']['version']}-" \
                                         F"cp3{minor_version}-" \
                                         F"abi3-" \
                                         F"{plattag}" \
                                         F".whl"

    if os.path.isdir(project_root + pyproject['project']['name']):
        module_root = project_root + pyproject['project']['name']
    elif os.path.isdir(project_root + os.path.join('src', pyproject['project']['name'])):
        module_root = project_root + os.path.join('src', pyproject['project']['name'])
    else:
        raise ModuleNotFoundError("Cannot find module source!")

    info_root = F"{pyproject['project']['name']}-{pyproject['project']['version']}.dist-info"

    with open(project_root + pyproject['project']['readme'], 'r') as fd:
        readme = fd.read()
        fd.close()

    metadata = ('METADATA', F"Metadata-Version: 2.1\n" \
                            F"Name: {pyproject['project']['name']}\n" \
                            F"Version: {pyproject['project']['version']}\n" \
                            F"Summary: {pyproject['project']['description']}\n" \
                            F"Home-page: {pyproject['project']['urls']['Repository']}\n" \
                            F"Author: {pyproject['project']['authors'][0]['name']}\n" \
                            F"Author-email: {pyproject['project']['authors'][1]['email']}\n" \
                            F"Project-URL: Bug Tracker, {pyproject['project']['urls']['Repository']}"
                            F"/issues\n" \
                            F"Classifier: Programming Language :: Python :: 3\n" \
                            F"Classifier: Operating System :: OS Independent\n" \
                            F"Requires-Python: {pyproject['project']['requires-python']}\n" \
                            F"Description-Content-Type: text/x-rst\n" \
                            F"License-File: LICENSE\n\n{readme}".encode('ascii', 'ignore'))
    # F"Classifier: License :: OSI Approved :: MIT License\n" \



    license = ('LICENSE', (
        lambda fd: (
            lambda read:
            fd.close() or read
        )(fd.read())
    )(open(project_root + 'LICENSE', 'rb')))

    wheel = ('WHEEL', F"Wheel-Version: 1.0\n" \
                      F"Generator: truckle (0.1.x)\n" \
                      F"Root-Is-Purelib: false\n" \
                      F"Tag: {plattag}\n\n".encode('ascii'))

    toplevel = ('top_level.txt', F"{pyproject['project']['name']}\n".encode())

    record = ('RECORD', b'')

    os.chdir(project_root)
    module_file_paths = glob.glob(os.path.join(module_root, '**', '*'), recursive=True)
    os.chdir(module_root)
    module_files = list(map(os.path.relpath,
                            glob.glob(os.path.join(module_root, '**', '*'), recursive=True)))

    module_data = [
        (filepath, open(filepath, 'rb').read())
        for filepath
        in module_files if os.path.isfile(filepath) and '__pycache__' not in filepath
    ]

    record = ('RECORD', '\n'.join(
        (lambda parent_dir: os.path.join(parent_dir, filename))(
            pyproject['project']['name'] if (i >= 5) else info_root  # 4 == len([m, w, tl, r, l])
        ) + ',sha256='
        + base64.urlsafe_b64encode(hashlib.sha256(contents).digest()).rstrip(b"=").decode()
        + ',' + str(len(contents))
        for i, (filename, contents)
        in reversed(list(enumerate(
            list(reversed([metadata, wheel, toplevel, record, license]))
            + module_data
        )))
    ))

    # # print(metadata)
    # # print(wheel)
    # # print(toplevel)
    # print(record)
    # print()



    module_files_not_pycache = [
        filepath
        for filepath
        in module_files if os.path.isfile(filepath) and '__pycache__' not in filepath
    ]

    files = [
            filepath
            for filepath
            in module_file_paths if os.path.isfile(filepath) and '__pycache__' not in filepath
        ]

    zf = zipfile.ZipFile(os.path.join(project_root, wheel_file_name), 'w')

    for file_relpath, file_path in zip(module_files_not_pycache, files):
        # print(file_path, os.path.join(pyproject['project']['name'], file_relpath))
        zf.write(file_path, os.path.join(pyproject['project']['name'], file_relpath))

    for file_relpath, file_contents in [metadata, wheel, toplevel, record, license]:
        # # print(len(file_contents), os.path.join(info_root, file_relpath))
        # # zf.writestr(file_contents, os.path.join(info_root, file_relpath))
        # print(os.path.join(info_root, file_relpath), len(file_contents))
        zf.writestr(os.path.join(info_root, file_relpath), file_contents)
    #
    # zf.close()
    #
    # zf = zipfile.ZipFile(os.path.join(project_root, wheel_file_name), 'r')
    #
    # for i in zf.infolist():
    #     print(f"is_dir: {i.is_dir()}; filename: {i.filename}")
    #
    # zf.close()
    #
    #
    print(F"`{pyproject['project']['name']}` v{pyproject['project']['version']} wheel built at {os.path.join(project_root, wheel_file_name)}")

    return os.path.join(project_root, wheel_file_name)


def greet(s: str) -> str:
    return F"Hello, {s}!"


if __name__ == "__main__":
    doctest.testmod()  # pragma: no cover
    # truckle('/Users/whowe/Documents/GitHub/mclbn256/setup.cfg')
    # truckle('/Users/whowe/Documents/GitHub/mclbn256/pyproject.toml')
    truckle('/Users/whowe/Documents/GitHub/truckle/pyproject.toml')
