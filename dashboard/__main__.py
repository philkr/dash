import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import argparse
from pathlib import Path
from . import plot, interface
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', nargs='+', default=[])
parser.add_argument('-r', '--remote')
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-u', '--update_interval', type=int, default=3600, help='In seconds')
parser.add_argument('-s', '--tabswitch_interval', type=int, default=10, help='In seconds')
parser.add_argument('-n', '--plots_per_line', type=int, default=3)

args = parser.parse_args()
app = dash.Dash(__name__, assets_folder=Path(__file__).parent / 'assets')

app.layout = html.Div(
    html.Div([
        html.Div(id='main-graphs'),
        dcc.Interval(
            id='interval-component',
            interval=args.update_interval*1000,  # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='ts-interval-component',
            interval=args.tabswitch_interval*1000,  # in milliseconds
            n_intervals=0
        ),
        html.Div(id='last-update'),
    ])
)

interfaces = []
for f in args.file:
    ti = interface.LocalSheetInterface(f)
    ti.poll()
    interfaces.append(ti)

if args.remote:
    ri = interface.RemoteSheetMultiInterface(args.remote)
    ri.poll()
    interfaces.append(ri)

@app.callback(Output('last-update', 'children'),
              [Input('interval-component', 'n_intervals')])
def update(n):
    for i in interfaces:
        i.poll()
    return ['last update: '+str(datetime.now())]


@app.callback(Output('main-graphs', 'children'),
              [Input('ts-interval-component', 'n_intervals')])
def tab_switch(n):
    r = []
    all_interfaces = []
    for i in interfaces:
        if isinstance(i, interface.Interface):
            all_interfaces.append(i)
        else:
            all_interfaces.extend(i.interfaces)
    for ti in all_interfaces:
        ti.poll()
        r.append(html.Div([html.H6(ti.name), plot.plot_tables(ti.tables, tid=n)],
                          style={'width': '%.2f%%' % (99 / args.plots_per_line), 'display': 'inline-block',
                                 'float': 'left', 'margin': '5px'}))
    return r


app.run_server(debug=args.debug)
