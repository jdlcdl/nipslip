import json
import time

import constants

def short_hex(some_bytes, prefix=8, suffix=4):
    if len(some_bytes):
        as_hex = some_bytes.hex()
        return as_hex[:prefix] + '..' + as_hex[len(as_hex)-suffix:]

def time_format(time_time):
    if time_time:
        return time.strftime('%c', time.gmtime(time_time))

def center_text(text, width):
    if len(text):
        return " "*((width-len(text))//2) + text

def show_event(event):
    fmt = "Event: {:18s}{:26s}at: {}\n   by: {}{}\n{}\n  sig: {}\n"
    if event.kind == 0:
        a_dict = json.loads(event.content)
        content = "\n".join(['       "{}: {}"'.format(k,v) for k,v in a_dict.items()])
    else:
        content = '       "' + event.content + '"'
    s = fmt.format(
        short_hex(event.id),
        center_text(constants.KINDS[event.kind], 26), 
        time_format(event.created_at),
        short_hex(event.pubkey.bytes()),
        "\n tags: " + "\n       ".join([str(x.serialize()) for x in event.tags]) if len(event.tags) else "",
        content,
        bool(event.sig)
    )
    return s

def show_filters(filters, indent=0):
    fmt = " "*indent + "{:>7s}: {}\n"
    s = ""
    if filters.ids:
        s += fmt.format("ids", filters.ids)
    if filters.authors:
        s += fmt.format("authors", [x.hex() for x in filters.authors])
    if filters.kinds:
        s += fmt.format("kinds", [constants.KINDS[x] for x in filters.kinds])
    if filters.etags:
        s += fmt.format("#e", [short_hex(x) for x in filters.etags])
    if filters.ptags:
        s += fmt.format("#p", [short_hex(x) for x in filters.ptags])
    if filters.since:
        s += fmt.format("since", time_format(filters.since))
    if filters.until:
        s += fmt.format("until", time_format(filters.until))
    if filters.limit:
        s += fmt.format("limit", filters.limit)
    return s

def show_subscription(subscription, filters_list):
    s = "Subscription: {}\n".format(subscription)
    for filters in filters_list:
        s += show_filters(filters, 1) + '\n'
    return s
