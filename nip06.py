"""
nostr nip06: basic key derivation from mnemonic seed phrase
"""

import bip340

def bip39_to_prvkey(mnemonic, passphrase=""):
    from embit import bip39, bip32
    seed = bip39.mnemonic_to_seed(mnemonic, passphrase)
    master = bip32.HDKey.from_seed(seed)
    derived = master.derive("m/44'/1237'/0'/0/0")
    return bip340.PrivateKey(derived.key.serialize())


if __name__ == '__main__':
    mnemonic = "day oak naive oak table ugly sad eager table habit ice sad"
    prvkey = bip39_to_prvkey(mnemonic)
    print("mnemonic: {}\nprvkey as hex: {}\npubkey as hex: {}\n".format(
          mnemonic,
          prvkey,
          prvkey.get_public_key(),
    ))
