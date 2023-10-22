"""
nostr nip13: proof of work
"""

import time
import json
import hashlib

import nip01


class NonceTag(nip01.Tag):
    def __init__(self, nonce, target):
        super().__init__("nonce", nonce, target)

def calc_difficulty(eventid):
    int_eventid = int.from_bytes(eventid, 'big')
    difficulty = 0
    for i in reversed(range(256)):
        if int_eventid < 2**i:
            difficulty += 1
    assert '{:0256b}'.format(int_eventid)[:difficulty] == "0"*difficulty
    return difficulty

def mine_event(event, target):
    for i, tag in enumerate(event.tags):
        if tag.tag == "nonce":
            event.tags.pop(i)
    prefix_delim = "NONCE"
    nonce_tag = NonceTag(prefix_delim, target)
    prefix = json.dumps([
        0,
        str(event.pubkey),
        event.created_at,
        event.kind,
        [i.serialize() for i in event.tags + [nonce_tag]]
    ], separators=(",", ":"))[:-1] + ","
    prefix = prefix.split(prefix_delim)
    suffix = json.dumps([
        event.content
    ], separators=(",", ";"))[1:]

    threshold = int(0xff**32 >> target).to_bytes(32, 'big')
    bprefix = bytes(prefix[0], 'utf-8')
    bsuffix = bytes(prefix[1] + suffix, 'utf-8')
    nonce = 0
    stime = time.time()
    while True:
        id_ = hashlib.sha256(
            bprefix + bytes(str(nonce), 'utf-8') + bsuffix
        ).digest()
        if id_ <= threshold:
            print('mined difficulty: {}, hps: {}, hash: {}'.format(
                calc_difficulty(id_), int(nonce/(time.time()-stime)), id_.hex()
            ))
            break
        if nonce % 1000000 == 0:
            print('mining target: {}, nonce: {}'.format(target, nonce))
        nonce += 1

    nonce_tag.subject = str(nonce)
    event.tags.append(nonce_tag)
    event.id = event.identify()
    return event
    

if __name__ == '__main__':
    import mock
    import output

    alice = mock.pubkey('alice')

    event = nip01.Event(alice, 1, 
        [nip01.PubkeyTag(alice)], 
        "Just talking to myself, and having difficulty."
    )
    print(output.show_event(event))

    diff = 20 
    mined = mine_event(event, diff)
    assert mined.id == mined.identify()
    print(output.show_event(mined))

