=======
truckle
=======

A simple setuptools alternative for packing Python modules (with or without FFI bindings) into
`wheels <https://en.wikipedia.org/w/index.php?title=Cheese_wheel&redirect=no&rtitle=Truckle>`__.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/truckle.svg
   :target: https://badge.fury.io/py/truckle
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/truckle/badge/?version=latest
   :target: https://truckle.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/wyatt-howe/truckle/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/wyatt-howe/truckle/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/wyatt-howe/truckle/badge.svg?branch=main
   :target: https://coveralls.io/github/wyatt-howe/truckle?branch=main
   :alt: Coveralls test coverage summary.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/truckle>`__::

    python -m pip install truckle

The library can be imported in the usual way::

    from truckle import truckle

Examples
^^^^^^^^

.. |truckle| replace:: ``truckle``
.. _truckle: https://truckle.readthedocs.io/en/0.1.0/_source/truckle.html#truckle.truckle.truckle

The function |truckle|_ can be used as follows:

    >>> path_to_wheel = truckle.truckle("/Documents/GitHub/mclbn256/")
    `mclbn256` v0.3.5 wheel built at /home/Documents/GitHub/mclbn256/mclbn256-0.3.5-cp39-abi3-macosx_12_0_arm64.whl
    >>> path_to_wheel
    '/home/Documents/GitHub/mclbn256/mclbn256-0.3.5-cp39-abi3-macosx_12_0_arm64.whl'

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__::

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__::

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details)::

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__::

    python src/truckle/truckle.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org>`__::

    python -m pip install .[lint]
    python -m pylint src/truckle

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/wyatt-howe/truckle>`__ for this library.

Versioning
^^^^^^^^^^
Beginning with version 0.1.0, the version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/truckle>`__ by a package maintainer. First, install the dependencies required for packaging and publishing::

    python -m pip install .[publish]

Ensure that the correct version number appears in the ``pyproject.toml`` file and in any links to this package's Read the Docs documentation that exist in this README document. Also ensure that the Read the Docs project for this library has an `automation rule <https://docs.readthedocs.io/en/stable/automation-rules.html>`__ that activates and sets as the default all tagged versions. Create and push a tag for this version (replacing ``?.?.?`` with the version number)::

    git tag ?.?.?
    git push origin ?.?.?

Remove any old build/distribution files. Then, package the source into a distribution archive using the `wheel <https://pypi.org/project/wheel>`__ package::

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__ using the `twine <https://pypi.org/project/twine>`__ package::

    python -m twine upload dist/*
