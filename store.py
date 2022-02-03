import plotly.graph_objects as go
from tasks.dictionaries import *


def get_cdm(dictionary):
	return {key: f'rgb{tuple(i)}' for key, i in dictionary.items()}


def get_experiment_name(city, experiment):
	if experiment == 'E0':
		return 'Baseline'
	elif (experiment == 'E1') & (city == 'Prince George'):
		return 'Prevailing Policy'
	elif (experiment == 'E1') & (city == 'Victoria'):
		return 'Dispersed'
	elif experiment == 'E2':
		return 'Neighbourhood Center'
	elif (experiment == 'E3') & (city != 'Vancouver'):
		return 'Corridor'
	elif (experiment == 'E3') & (city == 'Vancouver'):
		return 'Dispersed'
	elif experiment == 'E5':
		return 'Corridor'
	elif experiment == 'E6':
		return 'Transit-Oriented Development'
	else:
		return experiment


land_use_cdm = get_cdm(LAND_USE)
energy_cdm = get_cdm(ENERGY)
emissions_cdm = get_cdm(ENERGY)
proximity_cdm = get_cdm(PROXIMITY)

# Chart template
template = dict(
	layout=go.Layout(
		title_font=dict(family="Avenir", size=11),
		font=dict(family="Avenir", size=12),
		margin=dict(l=0, r=0, t=0, b=0),
		paper_bgcolor='rgba(0,0,0,0)',
		plot_bgcolor='rgba(0,0,0,0)',
		showlegend=False,
		yaxis=dict(visible=False),
		xaxis=dict(visible=False),
	),
)

# CSS
NAME_COL = {'width': '30%', 'display': 'inline-block'}
CHART_COL = {'width': '100%', 'display': 'inline-block'}
STD_ROW = {'width': '100%', 'height': '10%', 'display': 'inline-block'}
CHART_STYLE = {'height': '25px', 'margin-top': 0}
GRAPH_CONFIG = {'displayModeBar': False}
