# %%
import xarray as xr
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import cartopy.crs as ccrs
import plotly.express as px

# %%
# Download the data
ta_data = xr.open_dataset(
    "/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/tas_daily/r1i1p1f1/tas_day_MPI-ESM1-2-LR_r1i1p1f1_gn_18500501-18590930.nc"
)


# %%
# Function to prepare data for plotting
def prepare_data(ta_data):
    # Extract coordinates
    lon = ta_data.lon.values
    lat = ta_data.lat.values
    time = pd.to_datetime(ta_data.time.values)[:10]

    # Create a DataFrame with all points
    df = pd.DataFrame()
    for t in time:
        ta_values = ta_data["tas"].sel(time=t).values.flatten()
        lons_rep = np.repeat(lon, len(lat))
        lats_rep = np.tile(lat, len(lon))
        df_t = pd.DataFrame(
            {"lon": lons_rep, "lat": lats_rep, "ta": ta_values, "time": t}
        )
        df = pd.concat([df, df_t], ignore_index=True)

    return df, time


# Prepare the data
ta_df, time_values = prepare_data(ta_data)
# %%

# Create a Dash app for interactive visualization
app = Dash(__name__)

# Create the layout
app.layout = html.Div(
    [
        html.H1("Interactive Air Temperature Visualization"),
        html.Div(
            [
                dcc.Graph(id="ta-plot", style={"width": "100%", "height": "600px"}),
                html.Br(),
                html.Label("Time Range:"),
                dcc.RangeSlider(
                    id="time-slider",
                    min=0,
                    max=len(time_values) - 1,
                    value=[0, len(time_values) - 1],
                    marks={
                        i: str(time_values[i].date())
                        for i in range(0, len(time_values), len(time_values) // 10)
                    },
                ),
                html.Br(),
                html.Label("Time Step:"),
                dcc.Dropdown(
                    id="time-step",
                    options=[
                        {"label": "1 day", "value": 1},
                        {"label": "5 days", "value": 5},
                        {"label": "10 days", "value": 10},
                    ],
                    value=1,
                ),
                html.Button("Rotate View", id="rotate-button", n_clicks=0),
            ]
        ),
    ]
)


# Update the plot based on the time range
@app.callback(
    Output("ta-plot", "figure"),
    [
        Input("time-slider", "value"),
        Input("time-step", "value"),
        Input("rotate-button", "n_clicks"),
    ],
)
def update_plot(time_range, time_step, n_clicks):
    # Get the selected time range
    start_idx, end_idx = time_range
    selected_times = time_values[start_idx : end_idx + 1]

    # Create a figure
    fig = go.Figure()

    # Add base map (land and ocean)
    land_lon = ta_df["lon"][ta_df["ta"].isna()].values
    land_lat = ta_df["lat"][ta_df["ta"].isna()].values
    fig.add_trace(
        go.Scattergeo(
            lon=land_lon,
            lat=land_lat,
            marker=dict(color="lightgray", size=0.1, opacity=1),
            showlegend=False,
            name="Land",
        )
    )

    # Add temperature heatmap
    for t in selected_times[::time_step]:
        df_t = ta_df[ta_df["time"] == t]
        fig.add_trace(
            go.Scattergeo(
                lon=df_t["lon"].values,
                lat=df_t["lat"].values,
                text=df_t["ta"].values,
                marker=dict(
                    color=df_t["ta"].values,
                    colorscale="Jet",
                    cmin=250,
                    cmax=350,
                    colorbar=dict(title="Temperature (K)"),
                    opacity=0.8,
                    size=2,
                ),
                name=str(t.date()),
            )
        )

    # Update the layout
    fig.update_layout(
        title="Air Temperature",
        geo=dict(
            projection_type="orthographic",
            showland=True,
            showocean=True,
            landcolor="lightgray",
            oceancolor="skyblue",
        ),
        width=800,
        height=600,
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

# %%
