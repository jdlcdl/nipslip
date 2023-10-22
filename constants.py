"""
constants
"""

KINDS = {
    0: "Metadata", # nip01, nip05
    1: "Text", # nip01
    2: "Recommend Relay", # nip01
    3: "Contacts", # nip02
    4: "Encrypted Direct Messages", # nip04
    5: "Event Deletion", # nip09
    7: "Reaction", # nip25
    8: "Badge Award", # nip58
    40: "Channel Creation", # nip28
    41: "Channel Metadata", # nip28
    42: "Channel Message", # nip28
    43: "Channel Hide Message", # nip28
    44: "Channel Mute User", # nip28
    45: "Public Chat Reserved 45", # nip28
    46: "Public Chat Reserved 46", # nip28
    47: "Public Chat Reserved 47", # nip28
    48: "Public Chat Reserved 48", # nip28
    49: "Public Chat Reserved 49", # nip28
    1984: "Reporting", # nip56
    9734: "Zap Request", # nip57
    9735: "Zap", # nip57
    10002: "Relay List Metadata", # nip65
    22242: "Client Authentification", # nip42
    30008: "Profile Badges", # nip58
    30009: "Badge Definition", # nip58
    30023: "Long-form Content", # nip23
    30078: "Application-specific Data", # nip78
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
    "e": "event", # nip01, nip10
    "p": "pubkey", # nip01
    "r": "reference", # nip12
    "t": "hashtag", # nip12
    "g": "geohash", # nip12
    "nonce": "nonce", # nip13
    "subject": "subject", # nip14
    "d": "identifier", # nip33
    "expiration": "expiration", # nip40
}

MESSAGES = {
    "c2r": [
        "EVENT", # nip01
        "REQ", # nip01
#       "COUNT", # nip45
        "CLOSE", # nip01
        "AUTH" # nip42
    ],
    "r2c": [
        "EVENT", # nip01
        "NOTICE", # nip01
        "EOSE", # nip15
        "OK", # nip20
        "AUTH" # nip42
    ]
}


if __name__ == '__main__':
    print("Constants")
    print('{:>22s} {}'.format("len(KINDS):", len(KINDS)))
    print("{:>22s} {}".format("len(TAGS):", len(TAGS)))
    print("{:>22s} {}".format('len(MESSAGES["c2r"]):', len(MESSAGES["c2r"])))
    print("{:>22s} {}".format('len(MESSAGES["r2c"]):', len(MESSAGES["r2c"])))
    print()
