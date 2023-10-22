"""
nostr nip09: event deletion
"""

import nip01


class DeleteTag(nip01.Tag):
    def __init__(self, event):
        super().__init__("e", event)

def get_delete_event(pubkey, delete_tags, content=""):
    kind = 5
    return nip01.Event(pubkey, kind, delete_tags, content)


if __name__ == '__main__':
    import mock
    import output

    prvkey = mock.prvkey('Peter')
    pubkey = prvkey.get_public_key()

    events = [
        nip01.Event(pubkey, 1, [], "You are the Christ, the son of the living God."),
        nip01.Event(pubkey, 1, [], "Though they all fall away because of you, I will never fall away."),
        nip01.Event(pubkey, 1, [], "Even if I must die with you, I will not deny you!"),
    ]
        
    delete_tags = [DeleteTag(x.id) for x in events]
    events.append(get_delete_event(pubkey, delete_tags, ""))

    for event in events:
        print(output.show_event(event))
