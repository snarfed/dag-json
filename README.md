dag-json [![Circle CI](https://circleci.com/gh/snarfed/dag-json.svg?style=svg)](https://circleci.com/gh/snarfed/dag-json) [![Coverage Status](https://coveralls.io/repos/github/snarfed/dag-json/badge.svg?branch=main)](https://coveralls.io/github/snarfed/dag-json?branch=master)
===

Python implementation of the [IPLD](https://ipld.io/) [DAG-JSON codec](https://ipld.io/docs/codecs/known/dag-json/). Uses the [`CID`](https://multiformats.readthedocs.io/en/latest/cid.html) class from [`multiformats`](https://multiformats.readthedocs.io/). Passes all of IPLD's [DAG-JSON cross-codec test fixtures](https://ipld.io/specs/codecs/dag-json/fixtures/cross-codec/).

Install from [PyPI](https://pypi.org/project/dag-json/) with `pip install dag-json`.

License: This project is placed in the public domain. You may also use it under the [CC0 License](https://creativecommons.org/publicdomain/zero/1.0/).

* [Usage](#usage)
* [Changelog](#changelog)
* [Release instructions](#release-instructions)


## Usage

The `dag_json` module has three functions:
* `decode` takes DAG-JSON encoded `bytes` and returns the corresponding native Python object.
* `encode` takes any IPLD-compatible native Python object - `int`, `float`, `str`, `bool`, `list`, `bytes`, or [`multiformats.CID`](https://multiformats.readthedocs.io/en/latest/cid.html) - and returns it as DAG-JSON encoded `bytes`.
* `encoded_cid` takes DAG-JSON encoded `bytes` and returns its corresponding [`multiformats.CID`](https://multiformats.readthedocs.io/en/latest/cid.html).

Here's example usage:

```py
>>> from dag_json import decode, encode, encoded_cid
>>> from multiformats import CID

>>> encoded = encode({
    'foo': 'bar',
    'data': b'hello world',
    'link': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
})
>>> encoded
b'{"data":{"/":{"bytes":"aGVsbG8gd29ybGQ"}},"foo":"bar","link":{"/":"QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp"}}'

>>> repr(decode(encoded))
{
    'data': b'hello world',
    'foo': 'bar',
    'link': CID('base58btc', 0, 'dag-pb', '12205822d187bd40b04cc8ae7437888ebf844efac1729e098c8816d585d0fcc42b5b'),
}

>>> encoded_cid(encoded)
CID('base58btc', 1, 'dag-json', '1220d7c1db350b6fda1df4ab788bffc87b24c68d05ddfb2c9ff6f2a4f9eb12236c31')
```


## Changelog

### 0.2 - 2024-06-24

* Add new `encoded_cid` function.
* Add new `dialect` kwarg to `encode`, `DagJsonEncoder`. Currently only supports one value, `'atproto'`, to encode CIDs and bytes with `$link` and `$bytes` keys [according to the AT Protocol data model](https://atproto.com/specs/data-model).

### 0.1 - 2023-04-23

Initial release!


## Release instructions

Here's how to package, test, and ship a new release.

1. Run the unit tests.

    ```sh
    source local/bin/activate.csh
    python -m unittest discover
    ```
1. Bump the version number in `pyproject.toml`. `git grep` the old version number to make sure it only appears in the changelog. Change the current changelog entry in `README.md` for this new version from _unreleased_ to the current date.
1. `git commit -am 'release vX.Y'`
1. Upload to [test.pypi.org](https://test.pypi.org/) for testing.

    ```sh
    python -m build
    setenv ver X.Y
    twine upload -r pypitest dist/dag_json-$ver*
    ```
1. Install from test.pypi.org.

    ```sh
    cd /tmp
    python -m venv local
    source local/bin/activate.csh
    pip uninstall dag-json # make sure we force pip to use the uploaded version
    pip install --upgrade pip
    pip install -i https://test.pypi.org/simple --extra-index-url https://pypi.org/simple dag-json==$ver
    ```
1. [Run the example code above](#usage) to test that the code loads and runs.
1. Tag the release in git. In the tag message editor, delete the generated comments at bottom, leave the first line blank (to omit the release "title" in github), put `### Notable changes` on the second line, then copy and paste this version's changelog contents below it.

    ```sh
    git tag -a v$ver --cleanup=verbatim
    git push && git push --tags
    ```
1. [Click here to draft a new release on GitHub.](https://github.com/snarfed/dag-json/releases/new) Enter `vX.Y` in the _Tag version_ box. Leave _Release title_ empty. Copy `### Notable changes` and the changelog contents into the description text box.
1. Upload to [pypi.org](https://pypi.org/)!

    ```sh
    twine upload dist/dag_json-$ver.tar.gz dist/dag-json-$ver-py3-none-any.whl
    ```
