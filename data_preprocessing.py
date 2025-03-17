import zipfile
import pandas as pd
import json
import os

# Paths
zip_path = "Glacier.zip"
xlsx_path = "GTN Report.xlsx"
extract_dir = "glacier_data"
output_dir = "data"

# Create data directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process glacier data
glacier_data = []
region_coordinates = {
    '1_alaska': (64.2008, -149.4937), '2_western_canada_us': (52.9399, -106.4509),
    '3_arctic_canada_north': (75.0, -100.0), '4_arctic_canada_south': (65.0, -100.0),
    '5_greenland_periphery': (72.0, -40.0), '6_iceland': (64.9631, -19.0208),
    '7_svalbard': (78.0, 16.0), '8_scandinavia': (60.0, 15.0),
    '9_russian_arctic': (70.0, 100.0), '10_north_asia': (60.0, 90.0),
    '11_central_europe': (47.0, 10.0), '12_caucasus_middle_east': (42.0, 45.0),
    '13_central_asia': (43.0, 75.0), '14_south_asia_west': (35.0, 70.0),
    '15_south_asia_east': (27.0, 85.0), '16_low_latitudes': (0.0, -60.0),
    '17_southern_andes': (-40.0, -70.0), '18_new_zealand': (-41.2865, 174.7762),
    '19_antarctic_and_subantarctic': (-75.0, 0.0)
}

for file in os.listdir(extract_dir):
    if file.endswith('.csv') and file != '0_global.csv':
        region = file.replace('.csv', '')
        df = pd.read_csv(os.path.join(extract_dir, file))
        lat, lon = region_coordinates.get(region, (0, 0))
        for _, row in df.iterrows():
            glacier_data.append({
                "region": region,
                "start_date": row['start_dates'],
                "end_date": row['end_dates'],
                "glacier_area": row['glacier_area'],
                "glacier_mass_change": row['combined_gt'],
                "simulated_discharge": 500 * (1 - ((row['combined_gt'] - df['combined_gt'].min()) / (df['combined_gt'].max() - df['combined_gt'].min()))),
                "latitude": lat,
                "longitude": lon
            })

# Save glacier data to JSON
with open(os.path.join(output_dir, 'glacier_data.json'), 'w') as f:
    json.dump(glacier_data, f, indent=4)

# Convert GTN Report to JSON
df_gtn = pd.read_excel(xlsx_path)
df_gtn.to_json(os.path.join(output_dir, 'gtn_report.json'), orient='records', indent=4)

print("✅ Data successfully converted and saved in 'data/' directory.")
