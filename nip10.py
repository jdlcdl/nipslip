"""
nostr nip10: on "e" and "p" tags in text events
"""

import nip01


class RootTag(nip01.Tag):
    def __init__(self, event, relay=""):
        super().__init__("e", event, relay, "root")

class ReplyTag(nip01.Tag):
    def __init__(self, event, relay=""):
        super().__init__("e", event, relay, "reply")

class MentionTag(nip01.Tag):
    def __init__(self, event, relay=""):
        super().__init__("e", event, relay, "mention")

def get_reply_tags(pubkey, event_list):
    etags, ptags = [], []
    for event in event_list:
        if pubkey != event.pubkey:
            ptags.append(nip01.PubkeyTag(event.pubkey))
        if len([x for x in event.tags if x.tag=="e"]) == 0:
            etags.append(RootTag(event.id))
        else:
            etags.append(ReplyTag(event.id))
        for tag in [x for x in event.tags if x.tag=="p"]:
            if tag not in [x for x in ptags]:
                if tag.subject != pubkey.bytes():
                    ptags.append(tag)
    return etags + ptags

def get_quoted_event(pubkey, event):
    kind = 1
    tags = [MentionTag(event.id)]
    if pubkey != event.pubkey:
        tags.append(nip01.PubkeyTag(event.pubkey))
    for tag in [x for x in event.tags if x.tag=="p"]:
        if tag not in [x for x in tags]:
            if tag.tag != "p" or tag.subject != pubkey.bytes():
                tags.append(tag)
    return nip01.Event(pubkey, kind, tags, event.content)


if __name__ == '__main__':
    import mock 
    import output

    alice = mock.pubkey("alice")
    bob = mock.pubkey("bob")
    carol = mock.pubkey("carol")
    eve = mock.pubkey("eve")

    alice_post = nip01.Event(alice, 1, [], "I like freedom of expression, and Twitter.")

    print("--- via explicit tagging")
    bob_post = nip01.Event(bob, 1, [RootTag(alice_post.id), nip01.PubkeyTag(alice_post.pubkey)], 
        "Me too, but Twitter censors us."
    )
    carol_post = nip01.Event(carol, 1, [RootTag(alice_post.id), ReplyTag(bob_post.id), 
        *[nip01.PubkeyTag(x.pubkey) for x in [alice_post, bob_post]]], 
        "Let's learn to use nostr protocol instead!"
    )
    alice_post2 = nip01.Event(alice, 1, [RootTag(alice_post.id), ReplyTag(carol_post.id),
        ReplyTag(bob_post.id), *[nip01.PubkeyTag(x.pubkey) for x in [carol_post, bob_post]]],
        "Good idea Carol!  I agree with you Bob, Twitter does censor."
    )
    eve_post = nip01.Event(eve, 1, [MentionTag(carol_post.id),
        *[nip01.PubkeyTag(x.pubkey) for x in [alice_post, bob_post, carol_post]]], carol_post.content
    )
    for event in [alice_post, bob_post, carol_post, alice_post2, eve_post]:
        print(output.show_event(event))


    print("--- via nip10 helper functions")
    bob_post = nip01.Event(bob, 1, get_reply_tags(bob, [alice_post]), 
        "Me too, but Twitter censors us."
    )
    carol_post = nip01.Event(carol, 1, get_reply_tags(carol, [alice_post, bob_post]),
        "Let's learn to use nostr protocol instead!"
    )
    alice_post2 = nip01.Event(carol, 1, get_reply_tags(alice, [alice_post, bob_post, carol_post]),
        "Good idea Carol!  I agree with you Bob, Twitter does censor."
    )
    eve_post = get_quoted_event(eve, carol_post)
    for event in [alice_post, bob_post, carol_post, alice_post2, eve_post]:
        print(output.show_event(event))

