"""
nostr client
"""

import json
from binascii import unhexlify

import nip01


def get_keys(json_filename, private=False):
    import nip06
    import nip19
    private_key, public_key, previous_key = None, None, None

    f = open(json_filename)
    data = json.load(f)
    f.close()

    if private:
       if 'bip39_mnemonic' in data:
           mnemonic = data['bip39_mnemonic']
           if 'bip39_passphrase' in data:
               passphrase = data['bip39_passphrase']
           else:
               passphrase = ''
           private_key = nip06.bip39_to_prvkey(mnemonic, passphrase)
           public_key = private_key.get_public_key()

       if 'prvkey' in data:
           if private_key: previous_key = private_key
           private_key = nip01.PrivateKey(unhexlify(data['prvkey']))
           public_key = private_key.get_public_key()
           if previous_key:
               assert private_key == previous_key
               print('key:"prvkey" in "{}" is redundant.'.format(json_filename))

       if 'nsec' in data:
           if private_key: previous_key = private_key
           private_key = nip01.PrivateKey(nip19.from_bech32(data['nsec'])[1])
           if previous_key:
               assert private_key == previous_key
               print('key:"nsec" in "{}" is redundant.'.format(json_filename))

    else:
       if 'pubkey' in data:
           public_key = nip01.PublicKey.from_bytes(unhexlify(data['pubkey']))

       if 'npub' in data:
           if public_key: previous_key = public_key
           public_key = nip01.PublicKey.from_bytes(nip19.from_bech32(data['npub'])[1])
           if previous_key:
               assert public_key == previous_key
               print('key:"npub" in "{}" is redundant.'.format(json_filename))
        
    return private_key, public_key

def get_metadata(json_filename):
    f = open(json_filename)
    data = json.load(f)
    f.close()
    return data['metadata']
