#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash
import dash
import dash_leaflet as dl
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64
from animalShelter import AnimalShelter

# Database connection
username = "aacuser"
password = "SNHU1234"
shelter = AnimalShelter(username=username, password=password)

# Fetch initial data
df = pd.DataFrame.from_records(shelter.read({}))

# Set up the Dash app
app = JupyterDash('__name__')

# Load and encode the logo
image_filename = 'GraziosoSalvareLogo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Layout
app.layout = html.Div([
    html.Img(
        style={'width': '200px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'},
        src='data:image/png;base64,{}'.format(encoded_image.decode())
    ),
    html.Center(html.B(html.H2('SNHU CS-340 Grazioso Salvare Dashboard'))),
    html.Hr(),
    html.Div(
        className='row',
        style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'},
        children=[
            html.Div(children=[
                html.Button(id='button-one', n_clicks=0, children='Water Rescue'),
                html.Button(id='button-two', n_clicks=0, children='Mountain or Wilderness Rescue'),
                html.Button(id='button-three', n_clicks=0, children='Disaster Rescue or Individual Tracking'),
                html.Button(id='button-four', n_clicks=0, children='Reset'),
            ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px'})
        ]
    ),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_header={'backgroundColor': 'rgb(240,230,230)', 'fontWeight': 'bold'},
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        sort_action='native',
        filter_action='native',
        row_selectable='single',
        selected_rows=[],
    ),
    html.Br(),
    html.Hr(),
    html.Div(className='row', style={'display': 'flex', 'justifyContent': 'space-around'}, children=[
        html.Div(id='map-id', className='col s12 m6', style={'width': '45%'}),
        html.Div(id='pie-chart-id', className='col s12 m6', style={'width': '45%'})
    ]),
    html.Hr(),
    html.Div(id='bar-chart-container', style={'width': '70%', 'margin': '0 auto'})
])

@app.callback(
    Output('datatable-id', 'data'),
    [Input('button-one', 'n_clicks'),
     Input('button-two', 'n_clicks'),
     Input('button-three', 'n_clicks'),
     Input('button-four', 'n_clicks')]
)
def filter_data(btn1, btn2, btn3, btn4):
    # Detect which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return df.to_dict('records')
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Apply filter based on button clicked
    if button_id == 'button-one':
        query = {
            '$and': [
                {'breed': {'$in': ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']}},
                {'sex_upon_outcome': 'Intact Female'},
                {'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}}
            ]
        }
    elif button_id == 'button-two':
        query = {
            '$and': [
                {'breed': {'$in': ['German Shepherd', 'Alaskan Malamute', 'Old English Sheepdog']}},
                {'sex_upon_outcome': 'Intact Male'},
                {'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}}
            ]
        }
    elif button_id == 'button-three':
        query = {
            '$and': [
                {'breed': {'$in': ['Doberman Pinscher', 'German Shepherd', 'Golden Retriever']}},
                {'sex_upon_outcome': 'Intact Male'},
                {'age_upon_outcome_in_weeks': {'$gte': 20, '$lte': 300}}
            ]
        }
    else:  # Reset button or no filter
        query = {}

    data = shelter.read(query)
    return pd.DataFrame.from_records(data).to_dict('records')

@app.callback(
    Output('pie-chart-id', "children"),
    Input('datatable-id', "data")
)
def update_pie_chart(data):
    if not data or len(data) == 0:
        return []
    df = pd.DataFrame.from_dict(data)
    fig = px.pie(df, names='breed', title='Breed Distribution')
    return dcc.Graph(figure=fig)

@app.callback(
    Output('bar-chart-container', "children"),
    Input('datatable-id', "data")
)
def update_bar_chart(data):
    if not data or len(data) == 0:
        return []
    df = pd.DataFrame.from_dict(data)
    fig = px.bar(df, x='age_upon_outcome_in_weeks', y='breed', orientation='h', title='Age Distribution by Breed')
    return dcc.Graph(figure=fig)

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "data"),
     Input('datatable-id', "selected_rows")]
)


def update_map(viewData, index):
    if viewData is None or len(viewData) == 0:
        return dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75, -97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id")
        ])
    
    dff = pd.DataFrame.from_dict(viewData)
    if index is None or len(index) == 0:
        row = 0
    else:
        row = index[0]

    # Austin TX default coordinates
    lat, lon = 30.75, -97.48
    zoom = 10

    if len(dff) > 0 and row < len(dff):
        # Retrieve latitude and longitude from the data
        lat = dff.iloc[row, 13]  # Latitude column
        lon = dff.iloc[row, 14]  # Longitude column

        # Adjust zoom level if valid coordinates are found
        zoom = 13 if not pd.isna(lat) and not pd.isna(lon) else zoom
        
        return [
            dl.Map(style={'width': '1000px', 'height': '500px'},
                center=[lat, lon], zoom=zoom, children=[
                dl.TileLayer(id="base-layer-id"),
                dl.Marker(position=[lat, lon],
                    children=[
                        dl.Tooltip(dff.iloc[row, 4]),  # Animal breed
                        dl.Popup([
                            html.H1("Animal Name"),
                            html.P(dff.iloc[row, 9])  # Animal name
                        ])
                    ])
                ])
            ]
    else:
        # Default map view if data isn't valid
        return dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75, -97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id")
        ])
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)


# In[6]:


shelter = AnimalShelter(username = "aacuser", password = "SNHU1234")
data = shelter.read({})
data_list = list(data)
print(data_list[:10])


# In[ ]:




