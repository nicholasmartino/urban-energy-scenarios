import geopandas as gpd
import pandas as pd

DIRECTORY = "/Volumes/Samsung_T5/Databases/Sandbox/"
SANDBOXES = ["Hillside Quadra", "Sunset", "West Bowl"]

for sandbox in SANDBOXES:
	aggregated_mode_shifts = pd.DataFrame()
	df = pd.read_csv(f"{DIRECTORY}/{sandbox} - ModeShifts.csv")
	for experiment in df["Experiment"].unique():
		for mode in df["Mode"].unique():
			filtered_df = df.loc[(df["Experiment"] == experiment) & (df["Mode"] == mode)]
			aggregated_mode_shifts.loc[f"{sandbox} - {experiment}", mode] = filtered_df["∆"].mean()
	aggregated_mode_shifts.to_csv(f"{DIRECTORY}/{sandbox} - ModeShifts - Aggregate.csv")
