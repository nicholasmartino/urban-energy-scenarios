import geopandas as gpd
import pandas as pd

from dictionaries import *
from store import get_experiment_name


def get_d2use(gdf, land_use):
	return [geom.distance(gdf[gdf['landuse'].isin(land_use)].unary_union) for geom in gdf['geometry']]


def get_distance_to_bike(gdf, city, experiment):
	if LAYERS[city][experiment]['Roads'] != '':
		roads_gdf = gpd.read_file(f'{DIRECTORY}/{city}.gdb', layer=LAYERS[city][experiment]['Roads'])
		if 'Bikeways' in roads_gdf.columns:
			bike_gdf = roads_gdf[roads_gdf['Bikeways'] == 1].copy()
			bike_uu = bike_gdf.unary_union
		elif ('cycle_ocp' in roads_gdf.columns) & (experiment == 'E0'):
			bike_gdf = roads_gdf[roads_gdf['cycle_ocp'] == 'existing'].copy()
			bike_uu = bike_gdf.unary_union
		else:
			bike_gdf = roads_gdf[roads_gdf['cycle_2040'] == 1].copy()
			bike_uu = bike_gdf.unary_union
		bike_gdf.to_file(f'../data/shp/{city}_{experiment}_bike.shp')
		gdf['d2bk'] = [geom.distance(bike_uu) for geom in gdf['geometry']]
	else:
		print(f"Distance to cycling lanes not calculated for {experiment} of {city}")
	return gdf


def get_distance_to_transit(gdf, city, experiment):
	if LAYERS[city][experiment]['Transit'] != '':
		transit_gdf = gpd.read_file(f'{DIRECTORY}/{city}.gdb', layer=LAYERS[city][experiment]['Transit'])
		transit_gdf.to_file(f'../data/shp/{city}_{experiment}_transit.shp')
		if ('bus_2020' in transit_gdf.columns) & (experiment == 'E0'):
			transit_uu = transit_gdf[transit_gdf['bus_2020'] == 1].unary_union
		elif 'freqt_2040' in transit_gdf.columns:
			transit_uu = transit_gdf[transit_gdf['freqt_2040'] == 1].unary_union
		elif 'Transit' in transit_gdf.columns:
			transit_uu = transit_gdf[transit_gdf['Transit'] == 1].unary_union
		else:
			transit_uu = transit_gdf.unary_union
		gdf['d2tr'] = [geom.distance(transit_uu) for geom in gdf['geometry']]

	else:
		print(f"Distance to transit stops not calculated for {experiment} of {city}")
	return gdf


def convert_emissions(gdf, city):
	for em_col in ['em_ht_t', 'em_cl_t', 'em_eqp_t', 'em_dhw_t', 'em_lgt_t', 'ann_em_t']:
		if em_col not in gdf.columns:
			kg_col = f"{em_col.split('_t')[0]}_kg"
			assert kg_col in gdf.columns, AssertionError(
				f"No {em_col} or {kg_col} data for {layer} layer in {city} database")
			gdf[em_col] = gdf[kg_col] / 1000
	return gdf


def rename_columns(gdf):
	for new, old_columns in COLUMN_NAMES.items():
		common_cols = set(old_columns).intersection(set(gdf.columns))
		assert len(common_cols) > 0, AssertionError(f"No {new} data for {layer} layer in {city} database")
		for old in old_columns:
			if old in gdf.columns:
				gdf[new] = gdf[old]
	return gdf


if __name__ == '__main__':
	gdfs = gpd.GeoDataFrame()

	for city, experiments in LAYERS.items():
		for experiment, layer in experiments.items():
			exp_gdf = gpd.read_file(f'{DIRECTORY}/{city}.gdb', layer=layer['Buildings'])
			exp_gdf['city'] = city
			exp_gdf['experiment'] = experiment
			exp_gdf['exp_name'] = get_experiment_name(city, experiment)

			# Estimate distances to cycling lanes
			exp_gdf = get_distance_to_bike(exp_gdf, city, experiment)

			# Estimate distances to transit stops
			exp_gdf = get_distance_to_transit(exp_gdf, city, experiment)

			# Transform emissions kg data into tons
			exp_gdf = convert_emissions(exp_gdf, city)

			# Check if columns exist
			exp_gdf = rename_columns(exp_gdf)

			# Calculate distance indicators
			os_gdf = gpd.read_file(OPEN_SPACES, layer=f'{city.replace(" ", "")}').to_crs(26910)
			os_gdf_uu = os_gdf.unary_union
			exp_gdf['d2os'] = [geom.distance(os_gdf_uu) for geom in exp_gdf['geometry']]
			exp_gdf['d2cv'] = get_d2use(exp_gdf, ['CV'])
			exp_gdf['d2cm'] = get_d2use(exp_gdf, ['CM', 'MX'])

			gdfs = pd.concat([gdfs, exp_gdf])
	gdfs['bld_id'] = gdfs.reset_index(drop=True).index
	gdfs = gdfs.loc[:, list(COLUMN_NAMES.keys()) + ['d2tr', 'd2bk', 'd2cv', 'd2cm', 'd2os', 'city', 'experiment', 'geometry']]

	# Rename land use
	gdfs = gdfs.replace(RENAME)

	# Check for null values
	for col in gdfs.columns:
		nulls = gdfs[col].isna().sum()
		if nulls > 0:
			print(f"{nulls} null values in {col} column")
	gdfs.to_file(f"{DIRECTORY}/{BUILDINGS_FILE}.shp", driver='ESRI Shapefile')
