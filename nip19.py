"""
nostr nip19: bech32-encoded entities
"""

from binascii import hexlify, unhexlify
from bech32 import convertbits, bech32_encode, bech32_decode


def to_bech32(hrp, some_bytes):
    data5 = convertbits(some_bytes, 8, 5)
    return bech32_encode(hrp, data5)

def from_bech32(a_string):
    hrp, data5 = bech32_decode(a_string)
    data8 = convertbits(data5, 5, 8, pad=False)
    return hrp, b''.join([int(i).to_bytes(1, 'big') for i in data8])


if __name__ == '__main__':
    nsec = 'nsec180cvv07tjdrrgpa0j7j7tmnyl2yr6yr7l8j4s3evf6u64th6gkwsgyumg0'
    npub = 'npub180cvv07tjdrrgpa0j7j7tmnyl2yr6yr7l8j4s3evf6u64th6gkwsyjh6w6'
    note = 'note180cvv07tjdrrgpa0j7j7tmnyl2yr6yr7l8j4s3evf6u64th6gkws4c58hj'
    hexval = '3bf0c63fcb93463407af97a5e5ee64fa883d107ef9e558472c4eb9aaaefa459d'

    print("bytes: 0x{}\n nsec: {}\n npub: {}\n note: {}\n".format(
        hexval, 
        to_bech32('nsec', unhexlify(hexval)),
        to_bech32('npub', unhexlify(hexval)),
        to_bech32('note', unhexlify(hexval))
    ))

    assert from_bech32(nsec) == ('nsec', unhexlify(hexval))
    assert to_bech32('nsec', unhexlify(hexval)) == nsec

    assert from_bech32(npub) == ('npub', unhexlify(hexval))
    assert to_bech32('npub', unhexlify(hexval)) == npub

    assert from_bech32(note) == ('note', unhexlify(hexval))
    assert to_bech32('note', unhexlify(hexval)) == note
