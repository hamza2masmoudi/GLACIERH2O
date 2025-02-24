import dash
from dash import dcc, html, Input, Output
def trigger_event(event):
    pass
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import zipfile
import numpy as np




# Load and prepare data
zip_path = "Glacier.zip"
gtn_report_path = "GTN Report.xlsx"
extract_dir = "glacier_data"

# Extract glacier zip contents
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Load regional glacier CSV files and assign approximate coordinates for visualization
region_coordinates = {
    '1_alaska': (64.2008, -149.4937),
    '2_western_canada_us': (52.9399, -106.4509),
    '3_arctic_canada_north': (75.0000, -100.0000),
    '4_arctic_canada_south': (65.0000, -100.0000),
    '5_greenland_periphery': (72.0000, -40.0000),
    '6_iceland': (64.9631, -19.0208),
    '7_svalbard': (78.0000, 16.0000),
    '8_scandinavia': (60.0000, 15.0000),
    '9_russian_arctic': (70.0000, 100.0000),
    '10_north_asia': (60.0000, 90.0000),
    '11_central_europe': (47.0000, 10.0000),
    '12_caucasus_middle_east': (42.0000, 45.0000),
    '13_central_asia': (43.0000, 75.0000),
    '14_south_asia_west': (35.0000, 70.0000),
    '15_south_asia_east': (27.0000, 85.0000),
    '16_low_latitudes': (0.0000, -60.0000),
    '17_southern_andes': (-40.0000, -70.0000),
    '18_new_zealand': (-41.2865, 174.7762),
    '19_antarctic_and_subantarctic': (-75.0000, 0.0000)
}

# Load glacier data into a combined DataFrame
glacier_data = []
region_files = [file for file in os.listdir(extract_dir) if file.endswith('.csv') and file != '0_global.csv']
for file in region_files:
    region_name = file.replace('.csv', '')
    df_region = pd.read_csv(os.path.join(extract_dir, file))
    df_region['region'] = region_name
    df_region['latitude'], df_region['longitude'] = region_coordinates.get(region_name, (0, 0))
    glacier_data.append(df_region)

df_glacier_regions = pd.concat(glacier_data, ignore_index=True)

# Simulate river discharge based on glacier melt trends
def simulate_discharge(glacier_mass_loss):
    max_discharge = 500  # Max discharge in cubic meters per second
    normalized_loss = (glacier_mass_loss - glacier_mass_loss.min()) / (glacier_mass_loss.max() - glacier_mass_loss.min())
    simulated_discharge = max_discharge * (1 - normalized_loss) + np.random.normal(0, 10, size=len(glacier_mass_loss))
    return np.clip(simulated_discharge, 50, max_discharge)

# Enhance DataFrame with simulated discharge
df_glacier_regions['simulated_discharge'] = simulate_discharge(df_glacier_regions['combined_gt'])

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Glacier Melt Impact on Water Resources - Interactive Visualization"

# Layout with 3D globe map and a side chart for selected region details
app.layout = html.Div([
    html.H1("🌍 Glacier Melt and Water Resources Visualization",
            style={'textAlign': 'center', 'fontSize': '28px', 'marginBottom': '20px', 'color': '#2C3E50'}),

    html.Div([
        dcc.Graph(id='world-map-visualization', style={'height': '75vh', 'width': '65%', 'display': 'inline-block'}),
        dcc.Graph(id='region-detail-chart', style={'height': '75vh', 'width': '33%', 'display': 'inline-block', 'paddingLeft': '1%'})
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    html.Div([
        html.Label("⏩ Animation Speed:", style={'fontWeight': 'bold', 'fontSize': '16px'}),
        dcc.Slider(
            id='animation-speed',
            min=50,
            max=1000,
            step=50,
            value=300,
            marks={50: 'Fast', 500: 'Medium', 1000: 'Slow'},
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={'width': '60%', 'margin': 'auto', 'paddingTop': '20px'})
])

# Callback to update the 3D world map for smoother panning and zooming
@app.callback(
    Output('world-map-visualization', 'figure'),
    [Input('animation-speed', 'value')]
)
def update_world_map(animation_speed):
    min_size, max_size = 4, 15
    normalized_sizes = (
        (df_glacier_regions['glacier_area'] - df_glacier_regions['glacier_area'].min()) /
        (df_glacier_regions['glacier_area'].max() - df_glacier_regions['glacier_area'].min())
    )
    bubble_sizes = normalized_sizes * (max_size - min_size) + min_size

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lat=df_glacier_regions['latitude'],
        lon=df_glacier_regions['longitude'],
        mode='markers',
        marker=dict(
            size=bubble_sizes,
            color=df_glacier_regions['simulated_discharge'],
            colorscale='Viridis',
            cmin=df_glacier_regions['simulated_discharge'].min(),
            cmax=df_glacier_regions['simulated_discharge'].max(),
            showscale=True,
            colorbar=dict(title="Discharge (m³/s)", thickness=15, len=0.5),
            line=dict(width=0.4, color='DarkSlateGrey')
        ),
        text=df_glacier_regions.apply(lambda row: (
            f"Region: {row['region']}<br>Year: {row['end_dates']}<br>Glacier Area: {row['glacier_area']:.2f} km²<Br>Discharge: {row['simulated_discharge']:.2f} m³/s"
        ), axis=1),
        hoverinfo='text',
        customdata=df_glacier_regions[['region']]
    ))

    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor="rgb(230, 230, 230)",
        showocean=True,
        oceancolor="rgb(180, 210, 255)",
        showcountries=True,
        countrycolor="rgb(150, 150, 150)",
        center=dict(lat=20, lon=0),
        resolution=50,
    )

    fig.update_layout(
        title="🌍 3D Globe - Glacier Melt and Water Resources",
        margin=dict(l=0, r=0, t=40, b=0),
        dragmode='pan',
        geo=dict(
            projection_rotation=dict(lon=0, lat=0),
            projection_scale=0.9,
            lataxis=dict(range=[-90, 90]),
            lonaxis=dict(range=[-180, 180]),
        ),
        font=dict(family="Arial", size=13, color="#2C3E50"),
    )

    return fig

# Callback to update the region detail chart when a bubble is clicked
@app.callback(
    Output('region-detail-chart', 'figure'),
    [Input('world-map-visualization', 'clickData')]
)
def update_region_chart(clickData):
    if not clickData:
        return go.Figure(layout=dict(title="Select a region to see details", font=dict(size=14)))

    selected_region = clickData['points'][0]['customdata'][0]
    region_data = df_glacier_regions[df_glacier_regions['region'] == selected_region].sort_values(by='end_dates')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=region_data['end_dates'],
        y=region_data['combined_gt'],
        mode='lines+markers',
        name='Glacier Mass Change (Gt)',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=region_data['end_dates'],
        y=region_data['simulated_discharge'],
        mode='lines+markers',
        name='Simulated River Discharge (m³/s)',
        line=dict(color='green')
    ))

    fig.update_layout(
        title=f"Glacier Mass vs Water Discharge - {selected_region.replace('_', ' ').title()}",
        xaxis_title="Year",
        yaxis_title="Value",
        legend=dict(x=0.02, y=0.98),
        margin=dict(l=30, r=20, t=40, b=40),
        font=dict(family="Arial", size=12)
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)

