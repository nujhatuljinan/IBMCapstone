from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from dash import no_update

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Creating a range to use it on marks property
# On range slider
payload_range = [x for x in range(int(min_payload), int(max_payload)+1, 1000)]
if payload_range[-1]<max_payload:
    payload_range.append(payload_range[-1]+1000)

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options = [
                                                 {'label':'All Sites', 'value':'All Sites'},
                                                 {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                 {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                 {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                 {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}
                                                        ], 
                                             value = 'All Sites',
                                             placeholder="Select a launch site here",
                                             searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                marks={mark: f"{mark}kg" for mark in payload_range}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_graph1(inp1):
    if inp1 == 'All Sites':
        pie_df = spacex_df[spacex_df['class']==1]
        fig= px.pie(pie_df,names='Launch Site', values='class', title = f'Success rate of all sites')
    else:
        pie_df = spacex_df[spacex_df['Launch Site']==inp1]
        fig = px.pie(pie_df,names='class', title = f'Success rate of {inp1}')
        
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_graph2(inp1,inp2):
    if inp1=='All Sites':
        scat_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= inp2[0]) & (spacex_df['Payload Mass (kg)'] <= inp2[1])]
        fig = px.scatter(scat_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='All sites - payload mass between {:8,d}kg and {:8,d}kg'.format(int(inp2[0]),int(inp2[1])))
    else:
        scat_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= inp2[0]) & (spacex_df['Payload Mass (kg)'] <= inp2[1]) & (spacex_df['Launch Site']==inp1)]
        fig = px.scatter(scat_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Site {} - payload mass between {:8,d}kg and {:8,d}kg'.format(entered_site,int(inp2[0]),int(inp2[1])))
    return fig


# Run the app
if __name__=='__main__':
    app.run_server(port=4050)