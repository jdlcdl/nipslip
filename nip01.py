"""
nostr nip01: basic protocol flow
"""

from binascii import unhexlify
import json
import time
import hashlib

import constants
from bip340 import PrivateKey, PublicKey, Signature


def validated_event_id(event_id):
    if type(event_id) == str:
        assert event_id.lower() == event_id
        event_id = unhexlify(event_id)
    assert type(event_id) == bytes
    assert len(event_id) == 32
    return event_id

def validated_pubkey(pubkey):
    if type(pubkey) == str:
        assert pubkey.lower() == pubkey
        pubkey = unhexlify(pubkey)
    if type(pubkey) == bytes:
        pubkey = PublicKey.from_bytes(pubkey)
    return pubkey

def validated_kind(kind):
    if type(kind) == str:
        kind = int(kind)
    assert type(kind) == int
    assert kind in constants.KINDS
    return kind

def validated_tags(tags):
    assert type(tags) == list
    assert len(tags) >= 1
    for i, tag in enumerate(tags):
        assert type(tag) == list
        assert len(tag) == 3
        assert tag[0] in constants.TAGS
        if tag[0] == "e":
            tag[1] == validated_event_id(tag[1])
        elif tag[0] == "p":
            tag[1] == validated_pubkey(tag[1])
        tags[i] = tag
    return tags


class Tag:
    def __init__(self, tag, subject, *extras):
        self.tag = tag
        if tag == "e":
            self.subject = validated_event_id(subject)
        elif tag == "p":
            self.subject = validated_pubkey(subject).bytes()
        else:
            self.subject = subject
        self.extras = extras

    def serialize(self):
        return [
            self.tag, 
            self.subject.hex() if type(self.subject) == bytes else self.subject
        ] + [str(x) or "" for x in self.extras]

    def __eq__(self, other):
        return self.serialize() == other.serialize()

class EventTag(Tag):
    def __init__(self, event, relay=""):
        super().__init__("e", event, relay)

class PubkeyTag(Tag):
    def __init__(self, pubkey, relay=""):
        super().__init__("p", pubkey.bytes(), relay)


class Event:
    def __init__(self, pubkey, kind, tags, content, created_at=None, id_=None, sig=None):
        self.pubkey = validated_pubkey(pubkey)
        self.kind = validated_kind(kind)
        self.tags = [i for i in tags]
        self.content = content
        if created_at is None:
            self.created_at = int(time.time())
        else: 
            self.created_at = created_at
        if id_ is None:
            self.id = self.identify()
        else:
            assert id_ == self.identify()
            self.id = id_
        if sig:
            self.sign(sig)
        else:
            self.sig = None

    def identify(self):
        serialized = json.dumps([
            0,
            str(self.pubkey),
            self.created_at,
            self.kind,
            [i.serialize() for i in self.tags],
            self.content
        ], separators=(",", ":"))
        return hashlib.sha256(bytes(serialized, 'utf-8')).digest()

    def verify(self, sig):
        return self.pubkey.verify(sig, self.id)

    def sign(self, sig):
        assert self.verify(sig)
        self.sig = sig

    def serialize(self):
        return json.dumps({
            'id': self.id.hex(),
            'pubkey': str(self.pubkey),
            'created_at': self.created_at,
            'kind': self.kind,
            'tags': [i.serialize() for i in self.tags],
            'content': self.content,
            'sig': self.sig and self.sig.serialize().hex() or ""
        }, separators=(",", ":"))

    def __eq__(self, other):
        return self.serialize() == other.serialize()

def event_from_json(json_event):
    d = json.loads(json_event)
    return Event(
        d['pubkey'],
        d['kind'],
        [Tag(*tag) for tag in d['tags']],
        d['content'],
        created_at=d['created_at'],
        id_=unhexlify(d['id']),
        sig=Signature(unhexlify(d['sig']))
    )


class Filters:
    def __init__(self, 
        ids=None, 
        authors=None,
        kinds=None,
        etags=None,
        ptags=None,
        since=None, 
        until=None,
        limit=None
    ):
        self.ids = [bytes(x) for x in ids] if type(ids) == list else []
        self.authors = [bytes(x) for x in authors] if type(authors) == list else []
        self.kinds = [validated_kind(x) for x in kinds] if type(kinds) == list else []
        self.etags = [validated_event_id(x) for x in etags] if type(etags) == list else []
        self.ptags = [validated_pubkey(x).bytes() for x in ptags] if type(ptags) == list else []
        self.since = int(since) if since else None
        self.until = int(until) if until else None
        self.limit = int(limit) if limit else None

    def filter(self, event):
        if self.since and self.since > event.created_at: return
        if self.until and self.until < event.created_at: return
        if len(self.kinds) and event.kind not in self.kinds: return
        if len(self.etags):
            fail = True
            for etag in self.etags:
                if etag in [x.subject for x in event.tags if x.tag == "e"]:
                    fail = False
                    break
            if fail: return
        if len(self.ptags):
            fail = True
            for ptag in self.ptags:
                if ptag in [x.subject for x in event.tags if x.tag == "p"]:
                    fail = False
                    break
            if fail: return
        if len(self.ids):
            fail = True
            for id_ in self.ids:
                if id_ == event.id[:len(id_)]:
                    fail = False
                    break
            if fail: return
        if len(self.authors):
            fail = True
            for author in self.authors:
                if author == event.pubkey.bytes()[:len(author)]:
                    fail = False
                    break
            if fail: return
        return event
        
    def serialize(self):
        d = {}
        if len(self.ids): d['ids'] = [x.hex() for x in self.ids]
        if len(self.authors): d['authors'] = [x.hex() for x in self.authors]
        if len(self.kinds): d['kinds'] = self.kinds
        if len(self.etags): d['#e'] = [x.hex() for x in self.etags]
        if len(self.ptags): d['#p'] = [x.hex() for x in self.ptags]
        if self.since: d['since'] = self.since
        if self.until: d['until'] = self.until
        if self.limit: d['limit'] = self.limit
        return json.dumps(d, separators=(",", ":"))

    def __eq__(self, other):
        return self.serialize() == other.serialize()

def filters_from_json(json_filters):
    d = json.loads(json_filters)
    p = {}
    if 'ids' in d: p['ids'] = [unhexlify(x) for x in d['ids']]
    if 'authors' in d: p['authors'] = [unhexlify(x) for x in d['authors']]
    if 'kinds' in d: p['kinds'] = [validated_kind(x) for x in d['kinds']]
    if '#e' in d: p['etags'] = [validated_event_id(x) for x in d['#e']]
    if '#p' in d: p['ptags'] = [validated_pubkey(x) for x in d['#p']]
    if 'since' in d: p['since'] = int(d['since'])
    if 'until' in d: p['until'] = int(d['until'])
    if 'limit' in d: p['limit'] = int(d['limit'])
    return Filters(**p)

