import geopandas as gpd
import pandas as pd

from dictionaries import *
from store import get_experiment_name

bld_gdf = gpd.read_file(f'{DIRECTORY}/{BUILDINGS_FILE}.shp')
bld_ctr = bld_gdf.copy()
bld_ctr['geometry'] = bld_gdf.centroids.buffer(1)
gdfs = gpd.GeoDataFrame()
for city, experiments in PARCELS.items():
	for experiment, layer in experiments.items():
		exp_bld_ctr = bld_ctr.loc[(bld_ctr['city'] == city) & (bld_ctr['experiment'] == experiment)].copy()
		exp_gdf = gpd.read_file(f'{DIRECTORY}/{city}.gdb', layer=layer)
		exp_gdf['city'] = city
		exp_gdf['experiment'] = experiment
		exp_gdf['exp_name'] = get_experiment_name(city, experiment)
		exp_gdf['area'] = exp_gdf.area
		exp_gdf['floor_area'] = gpd.sjoin(exp_gdf, exp_bld_ctr)
		exp_gdf['fsr'] = exp_gdf.area
		gdfs = pd.concat([gdfs, exp_gdf])
gdfs['pcl_id'] = gdfs.reset_index(drop=True).index
bld_gdf['pcl_id'] = gpd.sjoin(bld_ctr, gdfs).groupby('bld_id').first()['pcl_id']
