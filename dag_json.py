"""DAG-JSON encoder and decoder.

https://ipld.io/docs/codecs/known/dag-json/
https://ipld.io/specs/codecs/dag-json/spec/
"""
from base64 import b64decode, b64encode
import json

from multiformats import CID, multihash


def decode(input):
    """Decodes DAG-JSON encoded data.

    Args:
      input: bytes, str, or decoded JSON object

    Returns:
      decoded IPLD object

    Raises:
      ValueError
      :class:`json.JSONDecodeError`
    """
    if isinstance(input, bytes):
        input = input.decode()

    if isinstance(input, str):
        input = json.loads(input)

    def _decode(input):
        if isinstance(input, dict):
            if input.keys() == set(('/',)):
                if isinstance(input['/'], str):
                    # link
                    return CID.decode(input['/'])
                elif (isinstance(input['/'], dict) and
                      input['/'].keys() == set(('bytes',))):
                    # IPLD DAG-JSON base64-encoded bytes don't have padding, but
                    # Python base64 lib expects it
                    return b64decode(input['/']['bytes'] + '==')

            # normal mapping
            return {k: _decode(v) for k, v in input.items()}

        if isinstance(input, list):
            return [_decode(v) for v in input]

        return input

    return _decode(input)


class DagJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles :class:`CID` and bytes."""

    def encode(self, val):
        if isinstance(val, float):
            # ugly, but I couldn't find a way to do this with a format string
            return format(val).replace('e-0', 'e-')

        return super().encode(val)

    def default(self, val):
        if isinstance(val, CID):
            assert val.version in (0, 1)
            return {'/': val.encode('base32') if val.version == 1 else val.encode()}
        elif isinstance(val, bytes):
            # Python base64 lib emits padding, IPLD DAG-JSON bytes don't
            return {'/': {'bytes': b64encode(val).decode().rstrip('=')}}

        return super().default(val)



def encode(val):
    """Encodes an IPLD object as DAG-JSON.

    Args:
      val: IPLD object

    Returns:
      bytes, DAG-JSON encoded object

    Raises:
      ValueError
      :class:`json.JSONEncodeError`
    """
    return DagJsonEncoder(separators=(',', ':'),
                          sort_keys=True,
                          ensure_ascii=False,
                          allow_nan=False,
                          ).encode(val).encode()

def encoded_cid(data):
    """Generates the :class:`CID` for a DAG-JSON encoded object.

    Args:
      data: bytes, encoded DAG-JSON

    Returns:
      :class:`CID`

    Raises:
      ValueError, if data is not bytes
    """
    if not isinstance(data, bytes):
        raise ValueError(f'Expected bytes, got repr(data)')

    return CID('base58btc', 1, 'dag-json', multihash.digest(data, 'sha2-256'))
