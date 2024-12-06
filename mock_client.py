"""
nostr mock_client
"""

if __name__ == '__main__':
    import json
    import time

    import constants
    import nip01
    import nip02
    import nip09
    import nip19
    import client
    import relay
    import output
    import mock


    unsigned = []

    # account keys
    try: 
        prvkey, pubkey = client.get_keys('private.json', True)
    except (FileNotFoundError, PermissionError): 
        prvkey, pubkey = client.get_keys('public.json', False)
    if prvkey:
        try:
            pubkey2 = client.get_keys('public.json', False)[1]
            assert pubkey2 == pubkey
        except (FileNotFoundError, PermissionError): pass
    print('Account\n  prvkey: {}\n  pubkey: {}\n          {}'.format(
        prvkey if prvkey else None, 
        pubkey,
        nip19.to_bech32('npub', pubkey.bytes())
    ))

    # relay
    my_relay = relay.Relay()
    subscription = 'myfeed'
    my_filters = {
        "my_posts": nip01.Filters(
             authors=[pubkey.bytes()[:10]], 
             since=time.time()-60*60*24,
             limit=3,
        ),
        "tagged_me": nip01.Filters(
             ptags=[pubkey.bytes()], 
             since=time.time()-60*60*24*7,
             limit=10, 
        ),
        "wot_hourly": nip01.Filters(
             kinds=[2,3],
             since=time.time()-60*60,
             limit=100,
        ),
    }
    print(output.show_subscription(subscription, 
        [x for x in my_filters.values()]
    ))
    my_relay.req(subscription, [x.serialize() for x in my_filters.values()])

    # metadata event
    try: metadata = client.get_metadata('public.json')
    except (FileNotFoundError, PermissionError): metadata = None
    if metadata:
        kind = 0
        event = nip01.Event(pubkey, kind, [], 
            json.dumps(metadata, separators=(",", ":"))
        )
        if prvkey:
            event.sign(prvkey.sign(event.id))
            my_relay.event(event.serialize())
        else: unsigned.append(event)

    # contacts event
    event = nip02.get_contact_list_event(pubkey, [
        nip02.ContactTag(pubkey.bytes(), "", "me"),
        nip02.ContactTag(mock.pubkey("alice"), "", "alice"),
        nip02.ContactTag(mock.pubkey("bob"), "", "bob"),
        nip02.ContactTag(mock.pubkey("carol"), "", "carol"),
    ])
    if prvkey:
        event.sign(prvkey.sign(event.id))
        my_relay.event(event.serialize())
    else: unsigned.append(event)

    # message events
    kind = 1
    event = nip01.Event(pubkey, kind, [], "Hello world!")
    if prvkey:
        event.sign(prvkey.sign(event.id))
        my_relay.event(event.serialize())
    else: unsigned.append(event)

    event = nip01.Event(pubkey, kind, [], "I shouldn't say this, but...")
    if prvkey:
        event.sign(prvkey.sign(event.id))
        my_relay.event(event.serialize())
    else: unsigned.append(event)
    event = nip09.get_delete_event(pubkey, [nip09.DeleteTag(event.id)], "Forget it!")
    if prvkey:
        event.sign(prvkey.sign(event.id))
        my_relay.event(event.serialize())
    else: unsigned.append(event)

    # show events
    if prvkey:
        relayed = my_relay.req(subscription)
        events = [nip01.event_from_json(x) for x in relayed]
    else:
        events = [x for x in unsigned]
    print('\n'.join(output.show_event(x) for x in events))
