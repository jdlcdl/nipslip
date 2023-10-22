"""
nostr bip340
"""

import embit.ec
import binascii


class PrivateKey(embit.ec.PrivateKey):
    def __init__(self, thirtytwobytes):
        if type(thirtytwobytes) == str and len(thirtytwobytes) == 64:
             thirtytwobytes = binascii.unhexlify(thirtytwobytes)
        super().__init__(thirtytwobytes)

    def sign(self, msg_hash):
        return self.schnorr_sign(msg_hash)

    def get_public_key(self):
        return PublicKey(embit.ec.secp256k1.ec_pubkey_create(self._secret))

    def __str__(self):
        return self.serialize().hex()


class PublicKey(embit.ec.PublicKey):
    @classmethod
    def from_bytes(cls, thirtytwobytes):
        if type(thirtytwobytes) == str and len(thirtytwobytes) == 64:
             thirtytwobytes = binascii.unhexlify(thirtytwobytes)
        return cls.from_xonly(thirtytwobytes)

    def bytes(self):
        return self.xonly()

    def verify(self, sig, msg_hash):
        return self.schnorr_verify(sig, msg_hash)

    def __str__(self):
        return self.serialize()[1:].hex()

    def __eq__(self, other):
        return self.xonly() == other.xonly() and type(other) == PublicKey


class Signature(embit.ec.SchnorrSig):
    pass


if __name__ == '__main__':
    import hashlib

    prv0 = PrivateKey(hashlib.sha256(b'Not a good private key').digest())
    prv1 = PrivateKey(hashlib.sha256(b'Not a good private key').hexdigest())
    assert prv0 == prv1

    pub0 = prv0.get_public_key()
    pub1 = prv1.get_public_key()
    pub2 = PublicKey.from_bytes(str(pub1))
    pub3 = PublicKey.from_bytes(pub2.bytes())
    assert pub0 == pub1 == pub2 == pub3

    hashed_message = hashlib.sha256(b'This message is not interesting').digest()
    sig0 = prv0.sign(hashed_message)
    sig1 = prv1.sign(hashed_message)
    assert sig0 == sig1
    assert pub2.verify(sig0, hashed_message)
    assert pub3.verify(sig1, hashed_message)
