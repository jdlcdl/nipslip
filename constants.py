"""
constants
"""

KINDS = {
    0: "Metadata", # nip01, nip05
    1: "Short Text Note", # nip01
    2: "Recommend Relay", # nip01
    3: "Contacts", # nip02
    4: "Encrypted Direct Messages", # nip04
    5: "Event Deletion", # nip09
    6: "Repost", # nip18
    7: "Reaction", # nip25
    8: "Badge Award", # nip58
    16: "Generic Repost", # nip18
    40: "Channel Creation", # nip28
    41: "Channel Metadata", # nip28
    42: "Channel Message", # nip28
    43: "Channel Hide Message", # nip28
    44: "Channel Mute User", # nip28
#   45: "Public Chat Reserved 45", # nip28
#   46: "Public Chat Reserved 46", # nip28
#   47: "Public Chat Reserved 47", # nip28
#   48: "Public Chat Reserved 48", # nip28
#   49: "Public Chat Reserved 49", # nip28
    1063: "File Metadata", # nip94
    1311: "Live Chat Message", # nip53
    1040: "OpenTimestamps", # nip03
    1984: "Reporting", # nip56
    1985: "Label", # nip32
    4550: "Community Post Approval", # nip72
    9041: "Zap Goal", # nip57
    9734: "Zap Request", # nip57
    9735: "Zap", # nip57
    10000: "Mute List", # nip51
    10001: "Pin List", # nip51
    10002: "Relay List Metadata", # nip65
    13194: "Wallet Info", # nip47
    22242: "Client Authentification", # nip42
    23194: "Wallet Request", # nip47
    23195: "Wallet Response", # nip47
    24133: "Nostr Connect", # nip46
    27235: "HTTP Auth", # nip98
    30000: "Categorized People List", # nip51
    30001: "Categorized Bookmark List", # nip51
    30008: "Profile Badges", # nip58
    30009: "Badge Definition", # nip58
    30017: "Create or update a stall", # nip15
    30018: "Create or update a product", # nip15
    30023: "Long-form Content", # nip23
    30024: "Draft Long-form Content", # nip23
    30078: "Application-specific Data", # nip78
    30311: "Live Event", # nip53
    30315: "User Statuses", # nip38
    30402: "Classified Listing", # nip99
    30403: "Draft Classified Listing", # nip99
    31922: "Date-based Calendar Event", # nip52
    31923: "Time-based Calendar Event", # nip52
    31924: "Calendar", # nip52
    31925: "Calendar Event RSVP", # nip52
    31989: "Handler recommendation", # nip89
    31989: "Handler information", # nip89
    34550: "Community Definition", # nip72
}
KINDS.update( # nip16
    {x: "Regular Event {} ".format(x) for x in range(1000, 10000) if x not in KINDS}
)
KINDS.update( # nip16
    {x: "Replaceable Event {} Reserved".format(x) for x in range(10000, 20000) if x not in KINDS}
)
KINDS.update( # nip16
    {x: "Ephemeral Event {} Reserved".format(x) for x in range(20000, 30000) if x not in KINDS}
)
KINDS.update( # nip33
    {x: "Parameter Replaceable Event {} Reserved".format(x) for x in range(30000, 40000) if x not in KINDS}
)

TAGS = {
    "e": "event", # nip01/10
    "p": "pubkey", # nip01/02
    "a": "coordinatess to an event", # nip01
    "d": "identifier", # nip01
    "alt": "summary", # nip31
    "g": "geohash", # nip52/12
    "i": "identity", # nip39
    "k": "kind number", # nip18/25/72
    "l": "label / label namespace", # nip32
    "L": "label namespace", # nip32
    "m": "MIME type", # nip94
    "r": "reference/relay URL", # nip65
    "t": "hashtag", # nip12
    "amount": "millisatoshis", # nip57
    "bolt11": "bolt11 invoice", # nip57
    "challenge": "challenge string", # nip42
    "content-warning": "content-warning", # nip36
    "delegation": "pubkey/conditions/delegation token", # nip26
    "description": "invoice/badge description", # nip57/58
    "emoji": "shortcode/image URL", # nip30
    "expiration": "expiration", # nip40
    "goal": "event id", # nip75
    "image": "image URL", # nip23/58
    "lnurl": "bech32 encoded lnurl", # nip57
    "location": "location string", # nip52/99
    "name": "badge name", # nip58
    "nonce": "nonce", # nip13
    "preimage": "hash of bolt11 invoice", # nip57
    "price": "price", # nip99
    "proxy": "proxy", # nip48
    "published_at": "unix timestamp", # nip23
    "relay": "relay URL", # nip57
    "relays": "relay list", # nip57
    "subject": "subject", # nip14
    "summary": "article summary", # nip23
    "thumb": "badge thumbnail", # nip58
    "title": "article title", # nip23
    "zap": "pubkey/relay URL", # nip57
}

MESSAGES = {
    "c2r": [
        "EVENT", # nip01
        "REQ", # nip01
        "CLOSE", # nip01
        "AUTH", # nip42
        "COUNT", # nip45
    ],
    "r2c": [
        "EOSE", # nip15
        "EVENT", # nip01
        "NOTICE", # nip01
        "OK", # nip20
        "AUTH", # nip42
        "COUNT", # nip45
    ]
}


if __name__ == '__main__':
    print("Constants")
    print('{:>22s} {}'.format("len(KINDS):", len(KINDS)))
    print("{:>22s} {}".format("len(TAGS):", len(TAGS)))
    print("{:>22s} {}".format('len(MESSAGES["c2r"]):', len(MESSAGES["c2r"])))
    print("{:>22s} {}".format('len(MESSAGES["r2c"]):', len(MESSAGES["r2c"])))
    print()
