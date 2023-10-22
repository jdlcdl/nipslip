"""
nostr relay
"""

import json

import nip01


class Relay:
    events = []
    subscriptions = {}

    def event(self, json_event):
        event = nip01.event_from_json(json_event)
        self.events.append(event)
        
    def req(self, subscription, json_filters_list=[]):
        if len(json_filters_list):
            filters_list = [nip01.filters_from_json(x) for x in json_filters_list]
            self.subscriptions[subscription] = filters_list
        else:
            try: filters_list = self.subscriptions[subscription]
            except KeyError: return False
        events = []
        for filters in filters_list:
            events.extend([x for x in filter(filters.filter, self.events) if x not in events])
        if filters.limit and len(events) > filters.limit:
            events = events[-filters.limit:]
        return [x.serialize() for x in events]

    def count(self, unused, json_filters_list):
        if len(json_filters_list):
            filters_list = [nip01.filters_from_json(x) for x in json_filters_list]
            events = []
            for filters in filters_list:
                events.extend([x for x in filter(filters.filter, self.events) if x not in events])
            return len(events)
        else:
            return False

    def close(self, subscription):
        if subscription in self.subscriptions:
            del self.subscriptions[subscription]
            return True
        else:
            return False
