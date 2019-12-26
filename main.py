import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="keys.json"

import pandas as pd
from bq_helper import BigQueryHelper
import plotly.graph_objs as go
from plotly.offline import plot

bq_assistant = BigQueryHelper('bigquery-public-data', 'nhtsa_traffic_fatalities')

QUERY = """
        SELECT state_number, consecutive_number, vehicle_number, contributing_circumstances_motor_vehicle 
        FROM `bigquery-public-data.nhtsa_traffic_fatalities.factor_2015`
        LIMIT 10000
        """
df = bq_assistant.query_to_pandas(QUERY)

state_group = df.groupby(['state_number'])
trace1_data = state_group['state_number'].count()
"""
Bar graph
"""
trace1 = go.Bar(
                    x = trace1_data.index
                    ,y = trace1_data.values
                    )
trace1_layout = go.Layout(title = 'Traffic fatalities'
              ,xaxis= dict(title= 'State')
              ,yaxis=dict(title='Number of vehicles')
             )
fig = dict(data = [trace1], layout = trace1_layout)
plot(fig)

"""
Pie graph
"""
vehicle_group = df.groupby(['vehicle_number'])

trace2_data = state_group['vehicle_number'].count()
trace2 = go.Pie(
                    title = 'Vehicles after accident'
                    ,labels = trace2_data.index
                    ,values = trace2_data.values
                    )
plot(go.Figure(trace2))

"""
Scatter graph
"""
vehicles_group = [
    df[df['vehicle_number'] == 1]
    ,df[df['vehicle_number'] == 5]
    ,df[df['vehicle_number'] == 6]
    ,df[df['vehicle_number'] == 4]
]
trace3_data = [element.groupby(["state_number"])["state_number"].count() for element in vehicles_group]

graph_1 = go.Scatter(
    x=trace3_data[0].index,
    y=trace3_data[0].values,
    name="vehicle number 1"
)

graph_2 = go.Scatter(
    x=trace3_data[1].index,
    y=trace3_data[1].values,
    name="vehicle number 5"
)

graph_3 = go.Scatter(
    x=trace3_data[2].index,
    y=trace3_data[2].values,
    name="vehicle number 6"
)

graph_4 = go.Scatter(
    x=trace3_data[3].index,
    y=trace3_data[3].values,
    name="vehicle number 4"
)

scatter_layout = dict(
    title='Accidents of different vehicle numbers in the states',
    xaxis=dict(title='state', ),
    yaxis=dict(title='vehicle number'),
)

plot(dict(data=[graph_1, graph_2, graph_3, graph_4], layout=scatter_layout))