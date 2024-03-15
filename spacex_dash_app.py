# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df.groupby("Launch Site", as_index=False)["Launch Site"].first()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',  options=[{'label': 'All Sites', 'value': 'ALL'},{'label': launch_sites.iloc[0,0], 'value': launch_sites.iloc[0,0]},
                                {'label': launch_sites.iloc[1,0], 'value': launch_sites.iloc[1,0]},
                                {'label': launch_sites.iloc[2,0], 'value': launch_sites.iloc[2,0]},
                                {'label': launch_sites.iloc[3,0], 'value': launch_sites.iloc[3,0]}], value="ALL", placeholder = "Select a Launch Site here searchable", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success luanches by site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        
        filtered_df = filtered_df.groupby("class")["class"].count()
        print(filtered_df)
        fig2 = px.pie(filtered_df, values='class', 
        names=filtered_df.index, 
        title='Total success for site ' + entered_site)
        return fig2
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def render_scatter_plot(entered_site,entered_range):
    print(entered_range)
    spacex_df_range = spacex_df[spacex_df["Payload Mass (kg)"] >= entered_range[0]]
    spacex_df_range = spacex_df_range[spacex_df_range["Payload Mass (kg)"] <= entered_range[1]]
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df_range, x='Payload Mass (kg)', y='class', color="Booster Version Category", title="Correlation between payload and success for all sites")
        return fig
    else: 
        filtered_data = spacex_df_range[spacex_df["Launch Site"]==entered_site]
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color="Booster Version Category", title="Correlation between payload and success for site " + entered_site )
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
