# Metadata
COLUMN_NAMES = {
	"landuse": ["landuse", "LANDUSE", "Landuse", "landuse_2"],
	"total_kwh": ["total_kWh"],
	"total_gj": ["total_GJ"],
	"eui_kwh": ["EUI_kWh"],
	"euc_kwh": ["EUC_kWh"],
	"heating_gj": ["heating_GJ_annual", "heating_GJ"],
	"cooling_gj": ["cooling_GJ_annual", "cooling_GJ"],
	"light_gj": ["lighting_GJ_annual", "lighting_G", "lighting_GJ"],
	"equip_gj": ["equipment_", "equip_GJ", "equipment_GJ_annual"],
	"dhw_gj": ["dhw_GJ_ann", "dhw_GJ_annual"],
	"res_count": ["res_count"],
	"res_units": ["res_units", "n_res_unit"],
	"floor_area": ["floor_area", "TFA"],
	"mx_stories": ["maxstories"],
	"height": ["Height", "Building_Height", "height", "BuidlingHeight", "building_h"],
	"laneway": ["laneway"],
	"age": ["age", "AGE"],
	"em_ht_t": ["em_ht_t"],
	"em_cl_t": ["em_cl_t"],
	"em_eqp_t": ["em_eqp_t"],
	"em_dhw_t": ["em_dhw_t"],
	"em_lgt_t": ["em_lgt_t"],
	"ann_em_t": ["ann_em_t"]
}
COLUMN_DESCRIPTIONS = {
	"landuse": "Land Use",
	"total_kwh": "Total Energy Consumption (kWh)",
	"total_gj": "Total Energy Consumption (GJ)",
	"eui_kwh": "Energy Use Intensity (kWh)",
	"euc_kwh": "Energy Use of Commercial (kWh)",
	"heating_gj": "Energy Use for Heading (GJ)",
	"cooling_gj": "Energy Use for Cooling (GJ)",
	"light_gj": "Energy Use for Lighting (GJ)",
	"equip_gj": "Energy Use for Equipments (GJ)",
	"dhw_gj": "Energy Use for Domestic Hot Water (GJ)",
	"res_count": "Residents Count",
	"res_units": "Number of Residential Units",
	"floor_area": "Total Floor Area",
	"mx_stories": "Maximum Number of Storeys",
	"height": "Building Height",
	"laneway": "Laneway Buildings",
	"age": "Building Age Category",
	"em_ht_t": "Emissions from Heating (tCO2)",
	"em_cl_t": "Emissions from Cooling (tCO2)",
	"em_eqp_t": "Emissions from Equipments (tCO2)",
	"em_dhw_t": "Emissions from Domestic Hot Water (tCO2)",
	"em_lgt_t": "Emissions from Lighting (tCO2)",
	"ann_em_t": "Total Annual Emissions"
}
RENAME = {
	"RS_SF_D": "SFD",
	"RS_MF_L": "MFL",
	"RS_SF_A": "SFA",
	"RS_MF_H": "MFH"
}

# Colors
LAND_USE = {
	"SFD": [255, 248, 165],
	"SFA": [240, 220, 33],
	"MFL": [164, 126, 0],
	"MFM": [176, 173, 0],
	"MFH": [92, 76, 0],
	"MX": [255, 127, 0],
	"IND": [128, 128, 128],
	"CM": [200, 90, 90],
	"CV": [100, 172, 190],
	"OS": [180, 210, 180],
}
ENERGY = {
	"Heating": [230, 150, 150],
	"Cooling": [210, 240, 210],
	"Equipments": [190, 190, 190],
	"Hot Water": [150, 200, 220],
	"Light": [230, 200, 80]
}
PROXIMITY = {
	"Open": [180, 210, 180],
	"Civic": [100, 172, 190],
	"Comm.": [200, 90, 90],
	"Bike": [240, 180, 0],
	"Transit": [150, 172, 190]
}

# Explorer
DIRECTORY = "/Volumes/SALA/Research/eLabs/50_projects/22_ESRI_Dashboard/Data"
BUILDINGS_FILE = "buildings_20220203"

# Machine learning
DEPENDENT = [
	"eui_kwh",
	"heating_gj",
	"cooling_gj",
	"light_gj",
	"equip_gj",
	"dhw_gj",
	"em_ht_t",
	"em_cl_t",
	"em_lgt_t",
	"em_eqp_t",
	"em_dhw_t",
]
EXPLANATORY = [
	"area",
	"perimeter",
	"height",
	"res_count",
	"res_units",
	"age",
]

# GeoDatabase layers
BUILDINGS = {
	"Prince George": {
		"E0": "s_200326_jk_udes_E0_2020_BLDGS",
		"E1": "s_200316_jk_E7_2050_PPOLICY_BLDGS_tech_shell",
		"E2": "s_200316_jk_E5_2050_NC_FOCUS_BLDGS_tech_shell",
		"E3": "s_200316_jk_E6_2050_COR_FOCUS_BLDGS_tech_shell"
	},
	"Vancouver": {
		"E0": "E0_2020_bldgs",
		# "E1": "E1_2030_D_bldgs",
		# "E2": "E2_2030_COR_A_bldgs",
		"E3": "E3_2040_D_bldgs",
		# "E4": "E4_2040_COR_A_bldgs",
		"E5": "E5_2040_COR_B_bldgs",
		"E6": "E6_2040_TOD_B_bldgs",
		# "E7": "E7_2050_COR_B_bldgs",
		# "E8": "E8_2050_TOD_B_bldgs"
	},
	"Victoria": {
		"E0": "s_jk_200717_HQ_E0_2020_BLDGS_1",
		"E1": "s_jk_200808_HQ_E1_2040_BLDGS_1",
		"E2": "s_jk_200816_HQ_E2_2040_BLDGS_1",
		"E3": "s_jk_200808_HQ_E3_2040_BLDGS_1"
	}
}
PARCELS = {
	"Prince George": {
		"E0": "s_200108_cc_E0_2020_PRCLS",
		"E1": "s_200117_cc_E7_2050_PPOLICY_PRCLS",
		"E2": "c_200114_E5_2050_FOCUS_PRCLS_polygons2",
		"E3": "s_200210_cc_E6_2050_COR_FOCUS_PRCLS"
	},
	"Vancouver": {
		"E0": "E0_2020_PRCLS",
		"E3": "E3_2040_D_PRCLS",
		"E5": "E4_2040_COR_A_PRCLS",
		"E6": "E6_2040_TOD_B_PRCLS",
	},
	"Victoria": {
		"E0": "s_yl_200619_HQ_E0_2020_PRCLS",
		"E1": "s_yl_200717_HQ_E1_2040_PRCLS",
		"E2": "s_yl_200728_HQ_E2_2040_PRCLS",
		"E3": "s_yl_200729_HQ_E3_2040_PRCLS"
	}
}
NETWORK = {
	"Prince George": {
		"E0": {
			"Roads": "s_200107_cc_E0_2020_ROADS",
			"Transit": "s_200214_cc_E0_2020_TRANSIT"
		},
		"E1": {
			"Roads": "s_200107_cc_E0_2020_ROADS",
			"Transit": "s_200225_cc_AT_2050_TRANSIT",
		},
		"E2": {
			"Roads": "s_200214_cc_AT_2050_ROADS",
			"Transit": "s_200225_cc_AT_2050_TRANSIT",
		},
		"E3": {
			"Roads": "s_200214_cc_AT_2050_ROADS",
			"Transit": "s_200225_cc_AT_2050_TRANSIT",
		}
	},
	"Vancouver": {
		"E0": {
			"Roads": "E0_streets",
			"Transit": "E0_streets"
		},
		"E3": {
			"Roads": "E0_streets",
			"Transit": "E0_streets"
		},
		"E5": {
			"Roads": "E0_streets",
			"Transit": "E0_streets"
		},
		"E6": {
			"Roads": "E0_streets",
			"Transit": "E0_streets"
		},
	},
	"Victoria": {
		"E0": {
			"Roads": "nm_200612_HQ_E0_2020_STRTS",
			"Transit": "nm_200612_HQ_E0_2020_INTRS"
		},
		"E1": {
			"Roads": "nm_200612_HQ_E0_2020_STRTS",
			"Transit": "nm_200612_HQ_E0_2020_INTRS"
		},
		"E2": {
			"Roads": "nm_200612_HQ_E0_2020_STRTS",
			"Transit": "nm_200612_HQ_E0_2020_INTRS"
		},
		"E3": {
			"Roads": "nm_200612_HQ_E0_2020_STRTS",
			"Transit": "nm_200612_HQ_E0_2020_INTRS"
		}
	}
}
OPEN_SPACES = f"{DIRECTORY}/Open Spaces.gdb"
