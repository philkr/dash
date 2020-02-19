import datetime
from typing import Dict


class Entry:
    name: str
    timestamp: datetime.datetime
    performance: float

    def __init__(self, name: str, performance: float, timestamp: datetime.datetime):
        self.name = name
        self.performance = performance
        self.timestamp = timestamp or datetime.datetime.now()


class Interface(object):
    def poll(self):
        pass


class TabularInterface(Interface):
    baselines: Dict[str, Entry]
    entries: Dict[str, Entry]
    axis_name: str = ''

    def __init__(self):
        self.baselines = {}
        self.entries = {}

    def add(self, e: Entry):
        self.entries[e.name] = e

    def add_baseline(self, e: Entry):
        self.baselines[e.name] = e

