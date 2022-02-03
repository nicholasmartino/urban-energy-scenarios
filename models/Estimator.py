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

	def get_total_residents(self):
		return int(self.df[(self.df['experiment'] == self.experiment) & (self.df['city'] == self.city)]['res_count'].sum())

	def get_total_dwellings(self):
		self.df['res_units'] = self.df['res_units'].astype(float)
		return int(self.df[(self.df['experiment'] == self.experiment) & (self.df['city'] == self.city)]['res_units'].sum())
