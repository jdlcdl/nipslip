"""
nostr nip04: encrypted direct message
"""

import pyaes
import base64

import nip01


def encrypt(plain_content, shared_key, iv, fill=b' '):
    plain = bytes(plain_content, 'utf8')
    plain = plain + fill*(16 - len(plain)%16)
    plains = [plain[i:i+16] for i in range(0, len(plain), 16)]
    aes = pyaes.AESModeOfOperationCBC(shared_key, iv)
    ciphers = [aes.encrypt(x) for x in plains]
    b64cipher = base64.b64encode(b''.join(ciphers)).decode('utf-8')
    b64iv = base64.b64encode(iv).decode('utf-8')
    return '{}?iv={}'.format(b64cipher, b64iv)

def decrypt(cipher_content, shared_key):
    cipher, iv = [base64.b64decode(x) for x in cipher_content.split('?iv=')]
    ciphers = [cipher[i:i+16] for i in range(0, len(cipher), 16)]
    aes = pyaes.AESModeOfOperationCBC(shared_key, iv)
    plains = [aes.decrypt(x) for x in ciphers]
    return b''.join(plains).decode('utf-8')

def get_event(from_pubkey, to_pubkey, cipher_content, tags=[]):
    kind = 4
    try: 
        if to_pubkey.bytes() not in [x.subject for x in tags if x.tag=="p"]:
            tags.append(nip01.PubkeyTag(to_pubkey))
    except AttributeError:
        tags.append(nip01.PubkeyTag(to_pubkey))
    return nip01.Event(from_pubkey, kind, tags, cipher_content)


if __name__ == '__main__':
    import random
    import time

    import mock
    import output

    # private stuff
    alice = mock.prvkey('alice')
    bob = mock.prvkey('bob')

    # embit added ecdh as of feb 11 2023
    #def get_shared_key(prv32, pub32):
    #    import secp256k1
    #    assert type(prv32) == bytes and len(prv32) == 32
    #    assert type(pub32) == bytes and len(pub32) == 32
    #    pub = secp256k1.PublicKey(b'\x02' + pub32, True)
    #    shared = pub.ecdh(prv32)
    #    return shared
    #
    #shared_alice = get_shared_key(alice.serialize(), bob.get_public_key().bytes())
    #shared_bob = get_shared_key(bob.serialize(), alice.get_public_key().bytes())
    #assert shared_alice == shared_bob
    shared_alice = alice.ecdh(bob.get_public_key())
    shared_bob = bob.ecdh(alice.get_public_key())
    assert shared_alice == shared_bob

    # back to public
    alice = alice.get_public_key()
    bob = bob.get_public_key()
     
    plain = "Hey Bob!  Can you keep a secret?"
    iv = random.Random(time.time()).randbytes(16)
    event = get_event(alice, bob, encrypt(plain, shared_alice, iv))
    print(output.show_event(event))
    print('Decrypted: {}\n'.format(decrypt(event.content, shared_bob)))

    plain = "Not sure Alice.  Are you going to have to kill me?"
    iv = random.Random(time.time()).randbytes(16)
    event = get_event(bob, alice, 
        encrypt(plain, shared_bob, iv),
        [nip01.EventTag(event.id)]
    )
    print(output.show_event(event))
    print('Decrypted: {}\n'.format(decrypt(event.content, shared_alice)))

