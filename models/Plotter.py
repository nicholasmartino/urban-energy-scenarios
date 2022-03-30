import os.path
from datetime import datetime

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from shapely import geometry
import seaborn as sns
from models.Estimator import Estimator, pct_change
from store import template, land_use_cdm, energy_cdm, emissions_cdm, proximity_cdm


def grid(gdf, cell_size):
	xmin, ymin, xmax, ymax = gdf.total_bounds
	grid_cells = []
	for x0 in np.arange(xmin, xmax + cell_size, cell_size):
		for y0 in np.arange(ymin, ymax + cell_size, cell_size):
			x1 = x0 - cell_size
			y1 = y0 + cell_size
			grid_cells.append(geometry.box(x0, y0, x1, y1))
	return gpd.GeoDataFrame(grid_cells, columns=['geometry'], crs=gdf.crs)


class Plotter:
	def __init__(self, df, city, experiment):
		self.df = df
		self.city = city
		self.experiment = experiment

	def _map_file_exists(self):
		if os.path.exists(self.get_map_file_name()):
			return True
		else:
			return False

	def filter_df(self):
		df = self.df.copy()
		return df[(df['city'] == self.city) & (df['experiment'] == self.experiment)].copy()

	def filter_city(self):
		df = self.df.copy()
		return df[df['city'] == self.city].copy()

	def get_map_file_name(self):
		return f'static/png/{self.city}_{self.experiment}.png'

	def plot_map_file(self, replace=False):
		if replace or (not self._map_file_exists()):
			df = self.filter_df()
			city_df = self.filter_city()
			cells = grid(city_df, 50)

			city_df_ctr = city_df.copy()
			city_df_ctr['geometry'] = city_df_ctr.centroid.buffer(1)
			e0_df = city_df_ctr[city_df_ctr['experiment'] == 'E0']
			ex_df = city_df_ctr[city_df_ctr['experiment'] == self.experiment]

			# Get number of residents in each cell on E0
			cells['res_count_E0'] = cells.sjoin(
				e0_df.loc[:, ['res_count', 'geometry']]
			).groupby('index_right', as_index=False).sum()['res_count']

			# Get number of residents in each cell on current experiment
			cells[f'res_count_{self.experiment}'] = cells.sjoin(
				ex_df.loc[:, ['res_count', 'geometry']]
			).groupby('index_right', as_index=False).sum()['res_count']

			# Calculate percentage change for each cell
			# cells['change'] = [
			# 	pct_change(old, new) for old, new in zip(cells['res_count_E0'], cells[f'res_count_{self.experiment}'])
			# ]
			cells['change'] = cells[f'res_count_{self.experiment}'] - cells['res_count_E0']
			cells.loc[cells['change'] < 0, 'change'] = 0
			cells['geometry'] = cells.centroid

			# Plot results
			fig, ax = plt.subplots()

			xlim = ([cells.total_bounds[0], cells.total_bounds[2]])
			ylim = ([cells.total_bounds[1], cells.total_bounds[3]])

			ax.set_xlim(xlim)
			ax.set_ylim(ylim)

			if sum(cells['change'] > 0):
				cells = cells.dropna()
				cells['change_n'] = (cells['change'] - cells['change'].min()) / (cells['change'].max() - cells['change'].min())
				sns.kdeplot(
					data=cells, x=cells.geometry.x, y=cells.geometry.y, fill=True, ax=ax, cmap='BuGn',
					weights=cells['change'], alpha=0.5
				)
			df.plot(ax=ax, color='gray')
			plt.axis('off')
			plt.tight_layout()
			plt.savefig(self.get_map_file_name(), transparent=True)
			print(f"{self.city} {self.experiment} density change range {cells['change'].min()} {cells['change'].max()}")
		return

	def plot_map(self):
		time = datetime.now()
		df = self.filter_df()
		df = df.to_crs(4326)
		fig = px.choropleth(df, geojson=df.geometry, locations=df.index, template=template)
		fig.update_geos(fitbounds="locations", visible=False)
		print(f"Map exported in {datetime.now() - time} seconds")
		return fig

	def plot_land_use(self):
		bld_df = self.filter_df()
		bld_df = bld_df.sort_values('landuse')
		lu_df = bld_df.groupby('landuse', as_index=False).sum()
		lu_df['y'] = 1
		lu_df[''] = lu_df['landuse'].replace({
			'CM': 'Commercial',
			'CV': 'Civic',
			'OS': 'Open Spaces',
			'SFD': 'Detached',
			'SFA': 'Attached',
			'MFL': 'Multi-Family Low-Rise',
			'MFM': 'Multi-Family Mid-Rise',
			'MFH': 'Multi-Family High-Rise',
			'MX': 'Mixed',
			'IND': 'Industrial'
		})
		lu_df[''] = [f'{i} ({int(area)}m²)' for i, area in zip(lu_df[''], lu_df['area'])]
		return px.bar(
			lu_df, x='area', y="y", color='landuse', orientation='h', template=template,
			color_discrete_map=land_use_cdm, hover_data={'landuse': False, 'area': False, 'y': False, '': True}
		)

	def plot_dwelling_mix(self):
		df = self.filter_df()
		return df

	def plot_energy(self):
		df = self.filter_df()
		energy = pd.DataFrame()
		for col in ['heating_gj', 'cooling_gj', 'light_gj', 'equip_gj', 'dhw_gj']:
			energy[col] = [df[col].sum()]
		energy = energy.transpose()
		energy['y'] = 1
		energy['tech'] = energy.index
		energy['gj'] = energy[0]
		energy['tech'] = energy['tech'].replace({
			'heating_gj': 'Heating', 'cooling_gj': 'Cooling', 'light_gj': 'Light', 'equip_gj': 'Equipments', 'dhw_gj': 'Hot Water'
		})
		energy[''] = [f"{t} ({round(gj/1000, 1)}TJ, {round(100 * (gj/sum(energy.gj)), 2)}%)" for t, gj in zip(energy.tech, energy.gj)]
		return px.bar(
			energy, x='gj', y='y', orientation='h', template=template, color='tech',
			color_discrete_map=energy_cdm, hover_data={'tech': False, 'gj': False, 'y': False, '': True}
		)

	def plot_emissions(self):
		df = self.filter_df()
		emissions = pd.DataFrame()
		for col in ['em_ht_t', 'em_cl_t', 'em_eqp_t', 'em_dhw_t', 'em_lgt_t']:
			emissions[col] = [df[col].sum()]
		emissions = emissions.transpose()
		emissions['y'] = 1
		emissions['t'] = emissions[0]
		emissions['tech'] = emissions.index
		emissions['tech'] = emissions['tech'].replace({
			'em_ht_t': 'Heating', 'em_cl_t': 'Cooling', 'em_eqp_t': 'Equipments', 'em_lgt_t': 'Light', 'em_dhw_t': 'Hot Water'
		})
		emissions[''] = [f"{t} ({int(co2)}tCO2/year, {round(100 * (co2/sum(emissions.t)), 2)}%)" for t, co2 in zip(emissions.tech, emissions.t)]
		return px.bar(
			emissions, x='t', y='y', orientation='h', template=template, color='tech',
			color_discrete_map=emissions_cdm, hover_data={'tech': False, 't': False, 'y': False, '': True}
		)

	def plot_radar(self):
		df = self.filter_df()
		d2_df = pd.DataFrame()
		for col in ['d2os', 'd2cv', 'd2cm']:
			i = len(d2_df)
			d2_df.loc[i, 'r'] = len(df[df[col] < 400])/len(df)
			d2_df.loc[i, 'theta'] = f'{col}_400'
		return px.line_polar(d2_df, r='r', theta='theta', range_r=[0.2, 1], line_close=True, template=template)

	def plot_proximity(self):
		# if self.experiment != 'E0':
			# df = self.df.copy()
			# chg_df = pd.DataFrame()
			# for col in ['d2os', 'd2cv', 'd2cm', 'd2bk', 'd2tr']:
			# 	if col not in df.columns:
			# 		df[col] = 0.05
			# 	i = len(chg_df)
			# 	# Get % of residents within 400m of each land use in the baseline
			# 	baseline = len(df[(df['experiment'] == 'E0') & (df['city'] == self.city) & (df[col] <= radius)])/len(df)
			# 	# Get % of residents within 400m of each land use in the scenario
			# 	scenario = len(df[(df['experiment'] == self.experiment) & (df['city'] == self.city) & (df[col] <= radius)])/len(df)
			# 	chg_df.loc[i, 'use'] = col
			# 	chg_df.loc[i, 'change'] = pct_change(baseline, scenario)
			# chg_df = chg_df.replace({'d2os': 'Open', 'd2cv': 'Civic', 'd2cm': 'Comm.', 'd2bk': 'Bike', 'd2tr': 'Transit'})
			# chg_df['change_sf'] = [f"{i}%" for i in chg_df['change']]
			# chg_df[''] = chg_df['use']

		if self.experiment != 'E0':
			estimator = Estimator(self.df.copy(), self.city, self.experiment)
			chg_df = estimator.get_change_proximity()

			fig = px.bar(
				chg_df, x='', y='change', template=template, title="Proximity, % of buildings in 400m of:",
				range_y=[-15, 15], text="change_sf", color_discrete_map=proximity_cdm, color='use'
			)
			fig.update_layout(margin=dict(l=0, r=10, t=30, b=10))
			fig.add_annotation(x=2, y=-16, text="", showarrow=False)
			fig.update_xaxes(visible=True, title="")
			fig.update_yaxes(visible=True, title="", showticklabels=False)
			return fig
