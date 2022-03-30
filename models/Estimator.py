import pandas as pd
import numpy as np


def pct_change(old, new):
	if old == 0:
		return np.nan
	else:
		return round(((new - old) / old) * 100, 1)


class Estimator:
	def __init__(self, df, city, experiment):
		self.df = df
		self.city = city
		self.experiment = experiment

	def get_change_dwellings(self):
		if self.experiment != 'E0':
			df = self.df.copy()
			baseline = df.loc[(df['experiment'] == 'E0') & (df['city'] == self.city), 'res_units'].sum()
			scenario = df.loc[(df['experiment'] == self.experiment) & (df['city'] == self.city), 'res_units'].sum()
			return pct_change(baseline, scenario)

	def get_change_emissions(self):
		if self.experiment != 'E0':
			df = self.df.copy()
			baseline = df.loc[(df['experiment'] == 'E0') & (df['city'] == self.city), 'ann_em_t'].sum()
			scenario = df.loc[(df['experiment'] == self.experiment) & (df['city'] == self.city), 'ann_em_t'].sum()
			return pct_change(baseline, scenario)

	def get_change_energy(self):
		if self.experiment != 'E0':
			df = self.df.copy()
			baseline = df.loc[(df['experiment'] == 'E0') & (df['city'] == self.city), 'total_gj'].sum()
			scenario = df.loc[(df['experiment'] == self.experiment) & (df['city'] == self.city), 'total_gj'].sum()
			return pct_change(baseline, scenario)

	def get_change_residents(self):
		if self.experiment != 'E0':
			df = self.df.copy()
			df['res_units'] = df['res_units'].astype(float)
			baseline = df.loc[(df['experiment'] == 'E0') & (df['city'] == self.city), 'res_count'].sum()
			scenario = df.loc[(df['experiment'] == self.experiment) & (df['city'] == self.city), 'res_count'].sum()
			return pct_change(baseline, scenario)

	def get_change_proximity(self, radius=600):
		if self.experiment != 'E0':
			df = self.df.copy()
			chg_df = pd.DataFrame()
			for col in ['d2os', 'd2cv', 'd2cm', 'd2bk', 'd2tr']:
				if col not in df.columns:
					df[col] = 0.05
				i = len(chg_df)
				# Get % of residents within 400m of each land use in the baseline
				baseline = len(df[(df['experiment'] == 'E0') & (df['city'] == self.city) & (df[col] <= radius)]) / len(
					df)
				# Get % of residents within 400m of each land use in the scenario
				scenario = len(
					df[(df['experiment'] == self.experiment) & (df['city'] == self.city) & (df[col] <= radius)]) / len(
					df)
				chg_df.loc[i, 'use'] = col
				chg_df.loc[i, 'change'] = pct_change(baseline, scenario)
			chg_df = chg_df.replace(
				{'d2os': 'Open', 'd2cv': 'Civic', 'd2cm': 'Comm.', 'd2bk': 'Bike', 'd2tr': 'Transit'})
			chg_df['change_sf'] = [f"{i}%" for i in chg_df['change']]
			chg_df[''] = chg_df['use']
			return chg_df

	def get_total_residents(self):
		return int(self.df[(self.df['experiment'] == self.experiment) & (self.df['city'] == self.city)]['res_count'].sum())

	def get_total_dwellings(self):
		self.df['res_units'] = self.df['res_units'].astype(float)
		return int(self.df[(self.df['experiment'] == self.experiment) & (self.df['city'] == self.city)]['res_units'].sum())
