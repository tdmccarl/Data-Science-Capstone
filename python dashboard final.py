# Import required libraries							
import pandas as pd							
import dash							
import dash_html_components as html							
import dash_core_components as dcc							
from dash.dependencies import Input, Output							
import plotly.express as px							
							
# Read the launch data into pandas dataframe							
spacex_df = pd.read_csv("spacex_launch_dash.csv")							
max_payload = spacex_df['Payload Mass (kg)'].max()							
min_payload = spacex_df['Payload Mass (kg)'].min()							
							
# Create a dash application							
app = dash.Dash(__name__)							
					
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                        options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                        ],
                                         value='ALL',
                                         placeholder="Select a launch site here",
                                         searchable=True
                                         ),

                                html.Br(),

                                # Pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # Slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 1000: '1000', 2000: '2000'							
                                                    , 3000: '3000', 4000: '4000', 5000: '5000'							
                                                    , 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # Scatter plot to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])



# Callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
   Output(component_id='success-pie-chart', component_property='figure'),
      Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df

    # For all sites
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches by Site')
        return fig
    # For a specific site
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts()
        fig = px.pie(values=success_counts, 
                     names=success_counts.index, 
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# Callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
   Output(component_id='success-payload-scatter-chart', component_property='figure'),
   [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    # Filter dataframe based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    # For all sites
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
                         color="Booster Version Category", 
                         title="Correlation between Payload and Success for All Sites")
    # For a specific site
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
                         color="Booster Version Category", 
                         title=f"Correlation between Payload and Success for {entered_site}")

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
