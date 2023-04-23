dag-json [![Circle CI](https://circleci.com/gh/snarfed/dag-json.svg?style=svg)](https://circleci.com/gh/snarfed/dag-json) [![Coverage Status](https://coveralls.io/repos/github/snarfed/dag-json/badge.svg?branch=main)](https://coveralls.io/github/snarfed/dag-json?branch=master)
===

Python implemention of the [IPLD](https://ipld.io/) [DAG-JSON codec](https://ipld.io/docs/codecs/known/dag-json/). Passes all of IPLD's [DAG-JSON cross-codec test fixtures](https://ipld.io/specs/codecs/dag-json/fixtures/cross-codec/).

Install from [PyPI](https://pypi.org/project/dag-json/) with `pip install dag-json`.

License: This project is placed in the public domain.

* [Usage](#client)
* [Changelog](#changelog)
* [Release instructions](#release-instructions)

## Usage

TODO


## Changelog

### 0.1 - unreleased

Initial release!


## Release instructions

Here's how to package, test, and ship a new release.

1. Run the unit tests.

    ```sh
    source local/bin/activate.csh
    python3 -m unittest discover
    ```
1. Bump the version number in `pyproject.toml`. `git grep` the old version number to make sure it only appears in the changelog. Change the current changelog entry in `README.md` for this new version from _unreleased_ to the current date.
1. `git commit -am 'release vX.Y'`
1. Upload to [test.pypi.org](https://test.pypi.org/) for testing.

    ```sh
    python3 -m build
    setenv ver X.Y
    twine upload -r pypitest dist/dag-json-$ver*
    ```
1. Install from test.pypi.org.

    ```sh
    cd /tmp
    python3 -m venv local
    source local/bin/activate.csh
    pip3 uninstall dag-json # make sure we force pip to use the uploaded version
    pip3 install --upgrade pip
    pip3 install -i https://test.pypi.org/simple --extra-index-url https://pypi.org/simple dag-json==$ver
    deactivate
    ```
1. Smoke test that the code trivially loads and runs.

    ```sh
    source local/bin/activate.csh
    python3
    # run test code below
    deactivate
    ```
    Test code to paste into the interpreter:

    ```py
    import dag_json

    TODO
    ```
1. Tag the release in git. In the tag message editor, delete the generated comments at bottom, leave the first line blank (to omit the release "title" in github), put `### Notable changes` on the second line, then copy and paste this version's changelog contents below it.

    ```sh
    git tag -a v$ver --cleanup=verbatim
    git push && git push --tags
    ```
1. [Click here to draft a new release on GitHub.](https://github.com/snarfed/dag-json/releases/new) Enter `vX.Y` in the _Tag version_ box. Leave _Release title_ empty. Copy `### Notable changes` and the changelog contents into the description text box.
1. Upload to [pypi.org](https://pypi.org/)!

    ```sh
    twine upload dist/dag-json-$ver.tar.gz dist/dag-json-$ver-py3-none-any.whl
    ```
