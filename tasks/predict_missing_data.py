import geopandas as gpd
import pandas as pd
from seaborn import jointplot
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from dictionaries import *

bld_gdf = gpd.read_file(f'{DIRECTORY}/{BUILDINGS_FILE}.shp')
bld_gdf['area'] = bld_gdf.area
bld_gdf['perimeter'] = bld_gdf.boundary.length
bld_gdf['age'] = bld_gdf['age'].fillna(0)

for var in DEPENDENT:
	nn = bld_gdf[~bld_gdf[var].isna()]

	# Construct regressor and fit data
	x_train, x_test, y_train, y_test = train_test_split(nn.loc[:, EXPLANATORY], nn[var], test_size=0.2, random_state=0)
	reg = RandomForestRegressor(random_state=0)
	reg.fit(x_train, y_train)

	# Test regression
	y_predicted = reg.predict(x_test)
	df = pd.DataFrame({f'{var}_true': y_test, f'{var}_predicted': y_predicted})
	plot = jointplot(data=df, x=f'{var}_true', y=f'{var}_predicted', kind="reg", scatter_kws={'alpha': 0.1})
	plot.ax_joint.annotate(
		f'R2 = {round(r2_score(y_test, y_predicted), 2)} | '
		f'rmse = {round(mean_squared_error(y_test, y_predicted, squared=False))}',
		xy=(1, max(plot.ax_marg_y.get_ylim()) * 0.9)
	)
	plot.savefig(f'../static/png/regression_{var}.png', dpi=300)

	# Predict missing data
	null_gdf = bld_gdf[bld_gdf[var].isna()]
	bld_gdf.loc[bld_gdf[var].isna(), var] = reg.predict(null_gdf.loc[:, EXPLANATORY])

bld_gdf.to_file(f'{DIRECTORY}/{BUILDINGS_FILE}_predicted.shp')
