import pandas as pd
import os

# Define the file paths
gtn_report_path = 'GTN Report.xlsx'
glacier_data_dir = './glacier_data'

# Load the GTN report
gtn_data = pd.read_excel(gtn_report_path)

# Prepare a dictionary for region-to-country mapping based on GTN report
region_to_country = {
    'alaska': 'US - UNITED STATES',
    'scandinavia': 'SE - SWEDEN',
    'new_zealand': 'NZ - NEW ZEALAND',
    'antarctic_and_subantarctic': 'AQ - ANTARCTICA',
    'russian_arctic': 'RU - RUSSIAN FEDERATION',
    'greenland_periphery': 'GL - GREENLAND',
    'iceland': 'IS - ICELAND',
    'svalbard': 'NO - NORWAY',
    'western_canada_us': 'CA - CANADA',
    'arctic_canada_north': 'CA - CANADA',
    'arctic_canada_south': 'CA - CANADA',
    'south_asia_east': 'IN - INDIA',
    'south_asia_west': 'PK - PAKISTAN',
    'central_asia': 'KZ - KAZAKHSTAN',
    'caucasus_middle_east': 'GE - GEORGIA',
    'central_europe': 'DE - GERMANY',
    'north_asia': 'CN - CHINA',
    'low_latitudes': 'BR - BRAZIL',
    'southern_andes': 'CL - CHILE'
}

# Initialize an empty list for storing region-country mapping
region_country_mapping = []

# Loop through each glacier CSV file in the directory
for file_name in os.listdir(glacier_data_dir):
    if file_name.endswith('.csv'):
        region_name = file_name.split('.')[0]
        # Check if region exists in the predefined mapping
        if region_name in region_to_country:
            country = region_to_country[region_name]
            region_country_mapping.append({'region': region_name, 'country': country})

# Create a DataFrame for region-country mapping
region_country_df = pd.DataFrame(region_country_mapping)

# Save the mapping to a CSV file
region_country_mapping_file = './data/region_to_country_mapping.csv'
region_country_df.to_csv(region_country_mapping_file, index=False)

print(f"Region to Country mapping saved to {region_country_mapping_file}")

# Now you can load this CSV into your project for future use
