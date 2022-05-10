from dictionaries import *
import geopandas as gpd

base_dir = "/Volumes/Samsung_T5/Databases/Sandbox"
files = [
	"Mode Shifts - Urban Blocks - Sunset.geojson",
	"Mode Shifts - Urban Blocks - West Bowl.geojson",
	"Mode Shifts - Urban Blocks - Hillside Quadra.geojson",
]
RS = 1
MODES = ['walk', 'bike', 'transit', 'drive']
buildings_gdf = gpd.read_file(f"{DIRECTORY}/buildings.shp")

for city, neighbourhood in NEIGHBOURHOODS.items():
	for experiment in LAYERS[city].keys():
		mob_gdf = gpd.read_feather(
			f"{base_dir}/{neighbourhood}/Regression/test_{experiment.lower()}_s{RS}_{neighbourhood}.feather")
		mask = ((buildings_gdf['city'] == city) & (buildings_gdf['experiment'] == experiment))
		exp_buildings = buildings_gdf[mask].copy()
		exp_buildings['geometry'] = exp_buildings.centroid.buffer(0.1)
		old_cols_mode = [f'{mode}_{experiment.lower()}_rf_{RS}_n' for mode in MODES]
		join = gpd.sjoin(
			exp_buildings.loc[:, ['bld_id', 'geometry']],
			mob_gdf.loc[:, old_cols_mode + ['geometry']]
		)\
			.groupby('bld_id', as_index=False)\
			.mean()
		for col, mode in zip(old_cols_mode, MODES):
			buildings_gdf.loc[mask, mode] = list(join[col])
			print(f"{city} {experiment} {mode}: {join[col].mean()}")

buildings_gdf.to_file(f"{DIRECTORY}/buildings_mob.shp")
print("Process finished")
