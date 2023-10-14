import math

import dash_bootstrap_components as dbc
import geopandas as gpd
from dash import dcc
from dash import html
from tqdm import tqdm

from models.Estimator import Estimator
from models.Plotter import Plotter
from store import *

buildings = gpd.read_file(f"{DIRECTORY}/{BUILDINGS_FILE}.shp")
buildings['area'] = buildings.area

rows = []
for row, city in tqdm(enumerate(['Prince George', 'Victoria', 'Vancouver'])):
	cols = []
	for col, experiment in enumerate(buildings['experiment'].unique()):
		df = buildings[(buildings['city'] == city) & (buildings['experiment'] == experiment)]
		if len(df) > 0:
			# Estimate data
			estimator = Estimator(buildings, city, experiment)
			if experiment == 'E0':
				energy = html.Small("Energy")
				emissions = html.Small("Emissions")
				residents = html.Small(f"{estimator.get_total_residents()} residents")
				dwellings = html.Small(f"{estimator.get_total_dwellings()} dwellings")
			else:
				energy = html.Small(f"Energy ({estimator.get_change_energy()}% from baseline)")
				emissions = html.Small(f"Emissions ({estimator.get_change_emissions()}% from baseline)")
				residents = html.Small(f"{estimator.get_total_residents()} residents (+{int(estimator.get_change_residents())}%)")
				dwellings = html.Small(f"{estimator.get_total_dwellings()} dwellings (+{int(estimator.get_change_dwellings())}%)")

			exp_name = get_experiment_name(city, experiment)
			plotter = Plotter(buildings, city, experiment)
			plotter.plot_map_file(replace=False)
			cols.append(
				dbc.Row(
					id=f'{city}_{experiment}_card',
					className='pretty_container',
					children=[
						dbc.Row([
							dbc.Col([
								html.P(
									f'{city} ({exp_name})',
									style={'text-align': 'left', 'width': '100%', 'margin-bottom': 0}
								),
							], style={'width': '95%'}),
							dbc.Col([
								html.Img(
									src='static/png/expand.png',
									style={
										'width': '20px',
										'height': '20px',
										'overflow': 'hidden',
										'opacity': 0.5
									}
								)
							])
						], style={'height': '8%'}),
						dbc.Row([
							dbc.Col([
								# dbc.Row([
								# 	html.P(f'{city}', style={'text-align': 'center', 'width': '100%', 'margin-bottom': 0}),
								# ]),
								# dbc.Row([
								# 	html.Small(f'{experiment}', style={'text-align': 'center', 'width': '100%', 'margin-top': 0}),
								# ]),
								html.Small("New buildings"),
								html.Img(
									src=f'static/png/{city}_{experiment}.png',
									style={
										'width': '130%',
										'height': '90%',
										'overflow': 'hidden',
										'margin': '-5% -20% 0 -20%'
									}
								),
								html.P(residents),
								html.P(dwellings)
							], style={'width': '36%', 'height': '100%'}),
							# dbc.Col([
							# 	html.P(f'{city}_{experiment}'),
							# 	html.P(residents),
							# 	html.P(dwellings)
							# ], style=NAME_COL),
							dbc.Col([
								html.Small("Land Use", style={'margin-bottom': 0}),
								dcc.Graph(
									id=f'{city}_{experiment}_land_use',
									figure=plotter.plot_land_use(),
									style=CHART_STYLE,
									config=GRAPH_CONFIG
								),
								energy,
								dcc.Graph(
									id=f'{city}_{experiment}_energy',
									figure=plotter.plot_energy(),
									style=CHART_STYLE,
									config=GRAPH_CONFIG
								),
								emissions,
								dcc.Graph(
									id=f'{city}_{experiment}_emissions',
									figure=plotter.plot_emissions(),
									style=CHART_STYLE,
									config=GRAPH_CONFIG
								),
								html.Hr(style={'margin-top': '5px', 'margin-bottom': '2px'}),
								dcc.Graph(
									id=f'{city}_{experiment}_proximity',
									figure=plotter.plot_proximity(),
									config=GRAPH_CONFIG,
									style={'height': '80%'}
								),
							], style={'width': '70%', 'height': '100%'}),
						], style={'height': '60%', 'width': '100%'}),
						html.Br(),
						dbc.Row([
							# dbc.Col([
							# 	html.Small('Land Use'),
							# ], style=NAME_COL),
							# dbc.Col([
							# 	dcc.Graph(
							# 		id=f'{city}_{experiment}_land_use',
							# 		figure=plotter.plot_land_use(),
							# 		style=CHART_STYLE,
							# 		config=GRAPH_CONFIG
							# 	),
							# ], style=CHART_COL)
						], style=STD_ROW),
						dbc.Row([
							# dbc.Col([energy], style=NAME_COL),
							dbc.Col([
								# energy,
								# dcc.Graph(
								# 	id=f'{city}_{experiment}_energy',
								# 	figure=plotter.plot_energy(),
								# 	style=CHART_STYLE,
								# 	config=GRAPH_CONFIG
								# ),
							], style=CHART_COL)
						], style=STD_ROW),
						dbc.Row([
							# dbc.Col([emissions], style=NAME_COL),
							# dbc.Col([
							# 	dcc.Graph(
							# 		id=f'{city}_{experiment}_emissions',
							# 		figure=plotter.plot_emissions(),
							# 		style=CHART_STYLE,
							# 		config=GRAPH_CONFIG
							# 	),
							# ], style=CHART_COL)
						], style=STD_ROW)
					],
					style={
						'className': 'pretty_container',
						'height': f'{int(math.floor(85 / len(buildings.city.unique())))}vh',
						'width': f'{int(math.floor(100 / len(df.experiment.unique())))}vw',
						'margin-left': '3px',
						'margin-right': '3px',
						'margin-bottom': '3px',
						'display': 'inline-block',
						'font-family': 'Avenir',
						'overflow': 'hidden',
					}
				)
			)
	rows.append(dbc.Row(cols))
scorecards = html.Div(rows)
