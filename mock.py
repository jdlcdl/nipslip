"""
nostr mock
"""

def prvkey(name):
    from nip01 import PrivateKey
    bname = bytes(name*32, 'utf-8')[:32]
    return PrivateKey(bname)

def pubkey(name):
    return prvkey(name).get_public_key()


if __name__ == '__main__':
    from binascii import unhexlify
    from nip19 import to_bech32
    print('Mock User Keys')
    for name in ['alice', 'bob', 'carol']:
        print(' mock keys for "{}":'.format(name))
        prv, pub = prvkey(name), pubkey(name)
        print('  prvkey: 0x{}\n  pubkey: 0x{}\n  nsec: {}\n  npub: {}\n'.format(
            prv,
            pub,
            to_bech32('nsec', unhexlify(str(prv))),
            to_bech32('npub', unhexlify(str(pub)))
        ))
