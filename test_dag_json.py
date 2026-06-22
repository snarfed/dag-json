"""Unit tests for dag_json.py.

Uses IPLD's DAG-JSON cross-codec test fixtures defined in ipld_fixtures.md,
which was copied on 2023-04-22 from:
https://github.com/ipld/ipld/blob/e57bc8a3a63112021eaec409689ab9794763c2e7/specs/codecs/dag-json/fixtures/cross-codec/index.md

https://ipld.io/specs/codecs/dag-json/fixtures/cross-codec/
https://github.com/ipld/codec-fixtures#generating-testmark-output-for-ipldio
https://github.com/warpfork/go-testmark#what-is-the-testmark-format

TODO: negative fixtures
https://github.com/ipld/codec-fixtures#negative-fixtures
"""
import collections
import json
import os
from pathlib import Path
from unittest import skip, TestCase

from multiformats import CID, multibase
import testmark

import dag_json


fixtures = testmark.parse(Path(os.path.dirname(__file__)) / 'ipld_fixtures.md')

# maps str name to dict with 'string', 'hexbytes', 'cid' keys
tests = collections.defaultdict(dict)
for key, val in fixtures.items():
    name, codec, type_ = str(key).split('/')
    if codec == 'dag-json':
        tests[name][type_] = val


def create_test_fn(test):
    def run(self):
        input = bytes.fromhex(test['bytes'])
        decoded = dag_json.decode(input.decode())
        encoded = dag_json.encode(decoded)
        self.assertEqual(test['string'].rstrip(), encoded.decode())

        expected_cid = CID.decode(multibase.decode(test['cid'].strip()))
        self.assertEqual(expected_cid, dag_json.encoded_cid(input))

    return run


DagJsonTest = type('DagJsonTest', (TestCase,), {
    f'test_{name.replace("-", "_")}': create_test_fn(test)
    for name, test in tests.items()
})


class DagJsonExtraTest(TestCase):
    maxDiff = None

    CID_STR = 'bafkreicqpqncshdd27sgztqgzocd3zhhqnnsv6slvzhs5uz6f57cq6lmtq'
    DECODED = {
        'cid': CID.decode(CID_STR),
        'bytes': b'asdf',
    }
    ENCODED = {
        'cid': {'$link': CID_STR},
        'bytes': {'$bytes': 'YXNkZg'},
    }

    def test_encode_dialect_atproto(self):
        self.assertEqual(self.ENCODED,
                         json.loads(dag_json.encode(self.DECODED, dialect='atproto')))

    def test_encode_dialect_atproto(self):
        self.assertEqual(self.DECODED,
                         dag_json.decode(self.ENCODED, dialect='atproto'))

@skip
class NegativeDagJsonTest(TestCase):
    """From the DAG-JSON cross-codec negative fixtures:
    https://github.com/ipld/codec-fixtures/tree/abdc5b85251ad39f47dc5a264be354b3283c8b3b/negative-fixtures/dag-json

    TODO
    """
    def test_duplicate_map_keys(self):
        with self.assertRaises(ValueError):
            print(dag_json.decode('{"foo":1,"foo":2,"bar":3}'))
