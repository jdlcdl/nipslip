"""
nostr nip02: contact list and petnames
"""

import nip01


class ContactTag(nip01.Tag):
    def __init__(self, pubkey, relay="", petname=""):
        super().__init__("p", pubkey, relay, petname)

def get_contact_list_event(pubkey, contact_tags):
    kind = 3
    return nip01.Event(pubkey, kind, contact_tags, "")


if __name__ == '__main__':
    import mock
    import output

    pubkey = mock.pubkey('alice')
    contacts = [
        ContactTag(pubkey, "", "me (alice)"),
        ContactTag(mock.pubkey('bob'), "", "bob"),
        ContactTag(mock.pubkey('carol'), "", "carol"),
        ContactTag(mock.pubkey('eve'), "", "eve"),
    ]
    event = get_contact_list_event(pubkey, contacts)
    
    print(output.show_event(event))
