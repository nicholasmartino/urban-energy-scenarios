
for task in [
	"1_clean_buildings_data",
	"2_predict_missing_data",
	"3_clean_parcels_data",
	"4_join_mobility_data"
]:
	exec(open(f'{task}.py').read())
