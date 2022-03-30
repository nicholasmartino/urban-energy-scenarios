import geopandas as gpd
import pandas as pd

from dictionaries import *
from store import get_experiment_name


bld_gdf = gpd.read_file(f'{DIRECTORY}/{BUILDINGS_FILE}.shp')
bld_gdf['bld_id'] = bld_gdf.reset_index(drop=True).index
bld_ctr = bld_gdf.copy()
bld_ctr['area'] = bld_ctr.area
bld_ctr['geometry'] = bld_gdf.centroid.buffer(1)
gdfs = gpd.GeoDataFrame()
for city, experiments in PARCELS.items():
	for experiment, layer in experiments.items():
		exp_bld_ctr = bld_ctr.loc[(bld_ctr['city'] == city) & (bld_ctr['experiment'] == experiment)].copy()
		exp_bld_ctr['volume'] = exp_bld_ctr['height'] * exp_bld_ctr['area']
		exp_pcl = gpd.read_file(f'{DIRECTORY}/{city}.gdb', layer=layer)
		exp_pcl.crs = 26910
		exp_pcl['pcl_id_exp'] = exp_pcl.reset_index(drop=True).index
		exp_pcl['city'] = city
		exp_pcl['experiment'] = experiment
		exp_pcl['exp_name'] = get_experiment_name(city, experiment)
		exp_pcl['area'] = exp_pcl.area
		exp_pcl['floor_area'] = gpd.sjoin(exp_pcl, exp_bld_ctr).groupby('pcl_id_exp').sum()['volume'] / 3
		exp_pcl['fsr'] = exp_pcl.area / exp_pcl['floor_area']
		gdfs = pd.concat([gdfs, exp_pcl])
gdfs['pcl_id'] = gdfs.reset_index(drop=True).index

for city, experiments in PARCELS.items():
	for experiment, layer in experiments.items():
		exp_bld_mask = ((bld_gdf['city'] == city) & (bld_gdf['experiment'] == experiment))
		exp_pcl_mask = ((gdfs['city'] == city) & (gdfs['experiment'] == experiment))
		exp_pcl = gdfs[exp_pcl_mask]
		exp_bld = bld_gdf[exp_bld_mask]
		exp_bld_ctr = exp_bld.copy()
		exp_bld_ctr['geometry'] = exp_bld.centroid.buffer(1)
		bld_gdf['exp_name'] = get_experiment_name(city, experiment)
		bld_gdf.loc[exp_bld_mask, 'pcl_id'] = exp_bld_ctr.loc[:, ['bld_id', 'geometry']]\
			.sjoin(exp_pcl)\
			.groupby('bld_id')\
			.first()['pcl_id']

# Export files
bld_gdf.to_file(f'{DIRECTORY}/buildings.shp')
gdfs.loc[:, [
	'pcl_id', 'city', 'experiment', 'exp_name', 'area', 'floor_area', 'fsr', 'geometry'
]].to_file(f'{DIRECTORY}/parcels.shp')
