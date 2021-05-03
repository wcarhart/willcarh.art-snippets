import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from pandas.io import gbq
from google.oauth2 import service_account

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

credentials = service_account.Credentials.from_service_account_file('/path/to/your/keyfile.json')

queries = {
    'top_types': 'SELECT type, COUNT(*) count FROM hacker_news_copy.full_201510 GROUP BY 1 ORDER BY 2 LIMIT 100',
    'counts': '''
        SELECT a.month month, stories, comments, comment_authors, story_authors
        FROM (
            SELECT FORMAT_TIMESTAMP('%Y-%m', time_ts) month, COUNT(*) stories, COUNT(DISTINCT author) story_authors
            FROM hacker_news_copy.stories
            GROUP BY 1
        ) a
        JOIN (
            SELECT FORMAT_TIMESTAMP('%Y-%m', time_ts) month, COUNT(*) comments, COUNT(DISTINCT author) comment_authors
            FROM hacker_news_copy.comments
            GROUP BY 1
        ) b
        ON a.month=b.month
        ORDER BY 1
    ''',
    'score_per_hour': '''
        SELECT FORMAT_TIMESTAMP("%h", TIMESTAMP_SECONDS(time-3600*7)) hour, COUNT(*) stories, AVG(score) avg_score, SUM(score)/COUNT(*) prob
        FROM hacker_news_copy.stories
        WHERE FORMAT_DATE("%Y", time_ts)="2015" AND score>30
        GROUP BY 1
        ORDER BY 1
    '''
}

dfs = {}
for query_name in queries:
    df = gbq.read_gbq(queries[query_name], project_id='<PROJECTNAME>', credentials=credentials)

    # we can also pickle our dataframes so we don't rerun the same queries over and over again
    # if you pickle your dataframes, don't forget to comment out the query execution above
    # df.to_pickle(f'{query_name}.pkl')
    
# if you pickled the dataframes, don't forget to unpickle them before continuing
# for query_name in queries:
#     dfs[query_name] = pd.read_pickle(f'{query_name}.pkl')

# 'top_types' table
table_label = html.Label("Hacker News BigQuery Public Dataset")
table = dt.DataTable(
    id='top_types-table',
    columns=[{'name': i, 'id': i} for i in dfs['top_types'].columns],
    data=dfs['top_types'].to_dict('records'),
    style_cell={'textAlign': 'left'},
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto'
    },
    fill_width=False
)

# 'counts' histogram
df = dfs['counts'].copy(deep=True)
df.set_index('month', inplace=True)
df = df.unstack().reset_index()
df.columns = ['category', 'month', 'value']
fig = px.bar(
    df,
    x='category',
    y='value',
    color='category',
    animation_frame='month',
    range_y=[0,df['value'].max()*1.1],
    title='Hacker News interactions over time, animated'
)
histogram = dcc.Graph(id='counts-histogram', figure=fig)

# 'counts' line chart
fig = go.Figure()
for category in ['stories', 'comments', 'comment_authors', 'story_authors']:
    fig.add_trace(go.Scatter(
        x=dfs['counts']['month'], y=dfs['counts'][category],
        mode='lines+markers',
        name=category
    ))
fig.update_layout(title='Hacker News interactions over time')
line = dcc.Graph(id='counts-line', figure=fig)

# build app layout
app.layout = html.Div([
    table_label,
    table,
    histogram,
    line
])

if __name__ == '__main__':
    app.run_server(debug=True)
