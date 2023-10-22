"""
nostr nip14: subject tag in text events
"""

import nip01


class SubjectTag(nip01.Tag):
    def __init__(self, subject):
        super().__init__("subject", subject)


if __name__ == '__main__':
    import mock
    import output

    prvkey = mock.prvkey('alice')
    pubkey = prvkey.get_public_key()

    event = nip01.Event(pubkey, 1, 
        [SubjectTag("A \"Subject\" Tag for Text Events")],
        "NIP-14 defines the use of the \"subject\" tag in text events, as first implemented in 'more-speech'.\n  You can read more about it by clicking: https://github.com/jdlcdl/nips/blob/master/14.md"
    )
        
    print(output.show_event(event))
