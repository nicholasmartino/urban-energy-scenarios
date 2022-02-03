import dash
from dash import html

from layouts.scorecards import scorecards

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    scorecards
])

if __name__ == '__main__':
    app.run_server(debug=False, host='localhost')
