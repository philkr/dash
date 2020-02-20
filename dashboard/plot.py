import dash_core_components as dcc
from . import interface
from typing import List


def s(s, max_len=20):
    if len(s) > max_len - 3:
        return s[:max_len-3]+'...'
    return s


def plot_table(tb: interface.Table):
    # Filter the entries
    sorted_entries = sorted(tb.entries, key=lambda e: e.timestamp)
    first_entries = sorted_entries[:-tb.settings.keep_last]
    last_entries = sorted_entries[-tb.settings.keep_last:]
    top_entries = sorted(first_entries, key=lambda e: e.value, reverse=not tb.settings.lower_better)
    shown_entries = top_entries[:tb.settings.keep_top] + last_entries
    if not shown_entries:
        return None
    # Plot the entries
    entries = [{'x': [e.timestamp], 'y': [e.value], 'type': 'scatter', 'name': s(e.name)} for e in shown_entries]

    # Plot the baselines
    mn, mx = min(e.timestamp for e in shown_entries), max(e.timestamp for e in shown_entries)
    baselines = [{'x': [mn, mx], 'y': [e.value, e.value], 'name': s('b:' + e.name), 'mode': 'lines',
                  'line': dict(dash='dash')} for e in tb.baselines]
    return dcc.Graph(
        figure={
            'data': baselines + entries,
            'layout': {
                'title': {'text': tb.settings.name},
                'yaxis': {'title': {'text': tb.settings.axis},},
                'margin': dict(l=40, r=0, b=20, t=50, pad=2),
            },
        },
    )


def plot_tables(tbs: List[interface.Table], tid:int):
    tabs = []
    for tb in sorted([tb for tb in tbs if not tb.settings.hide], key=lambda tb: tb.settings.priority, reverse=True):
        plt = plot_table(tb)
        if plt is not None:
            tabs.append(dcc.Tab(label=tb.settings.name, children=[plt], value='t-%d' % len(tabs)))
    return dcc.Tabs(tabs, value='t-%d' % (tid % len(tabs)))
