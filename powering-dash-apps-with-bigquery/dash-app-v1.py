import dash
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Hello, Dash!', id='app-title'),
    html.Button('Change title', id='change-btn', n_clicks=0)
])

@app.callback(
	Output('app-title', 'children'),
    Input('change-btn', 'n_clicks')
)
def update_graph(n_clicks):
    if n_clicks % 2 == 0:
        return 'Hello, Dash!'
    return 'Hi there! Thanks for updating the title!'

if __name__ == '__main__':
    app.run_server(debug=True)
