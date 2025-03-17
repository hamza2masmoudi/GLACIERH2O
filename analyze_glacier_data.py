import pandas as pd
import json
# Generate visualizations and display them directly to the user using ace_tools
import ace_tools as tools
import matplotlib.pyplot as plt


# Load the glacier data
with open('/Users/hamza/glacier/data/glacier_data.json', 'r') as file:
    glacier_data = json.load(file)

# Load the GTN report data
with open('/Users/hamza/glacier/data/gtn_report.json', 'r') as file:
    gtn_report = json.load(file)

# Convert to DataFrames for easier manipulation
glacier_df = pd.DataFrame(glacier_data)
gtn_df = pd.DataFrame(gtn_report)

# Extract unique regions from glacier data
unique_regions = glacier_df['region'].unique()

# Mapping countries from GTN report to corresponding glacier regions manually
region_country_mapping = {
    "1_alaska": ["US - UNITED STATES"],
    "2_western_canada_us": ["CA - CANADA", "US - UNITED STATES"],
    "3_arctic_canada": ["CA - CANADA"],
    "4_greenland": ["GL - GREENLAND"],
    "5_iceland": ["IS - ICELAND"],
    "6_svalbard_jan_mayen": ["SJ - SVALBARD AND JAN MAYEN"],
    "7_scandinavia": ["NO - NORWAY", "SE - SWEDEN", "FI - FINLAND"],
    "8_russian_arctic": ["RU - RUSSIAN FEDERATION"],
    "9_siberia": ["RU - RUSSIAN FEDERATION"],
    "10_central_asia": ["KZ - KAZAKHSTAN", "TJ - TAJIKISTAN", "UZ - UZBEKISTAN", "KG - KYRGYZSTAN"],
    "11_himalaya": ["NP - NEPAL", "IN - INDIA", "CN - CHINA", "BT - BHUTAN", "PK - PAKISTAN"],
    "12_caucasus_middle_east": ["GE - GEORGIA", "TR - TURKEY", "IR - IRAN"],
    "13_southern_andes": ["CL - CHILE", "AR - ARGENTINA"],
    "14_new_zealand": ["NZ - NEW ZEALAND"],
    "15_africa": ["MA - MOROCCO"],
    "16_antarctic": ["AQ - ANTARCTICA"],
}

# Assign regions to the GTN report based on country mapping
def assign_region(country_code):
    for region, countries in region_country_mapping.items():
        if country_code in countries:
            return region
    return "Unknown"

gtn_df['region'] = gtn_df['GRDCCOUNTRY'].apply(assign_region)

# Merge glacier data with GTN report based on 'region'
merged_df = pd.merge(glacier_df, gtn_df, on='region', how='inner')

import ace_tools as tools; tools.display_dataframe_to_user(name="Merged Glacier and GTN Data", dataframe=merged_df)

# Display the first few rows of the merged dataframe
merged_df.head()



# Plot 1: Glacier Mass Change vs Station Elevation
fig1, ax1 = plt.subplots(figsize=(12, 8))
ax1.scatter(merged_df['glacier_mass_change'], merged_df['station_elevation'], alpha=0.7, edgecolors='k', s=80)
ax1.set_title('Glacier Mass Change vs Station Elevation', fontsize=14)
ax1.set_xlabel('Glacier Mass Change (Gt)', fontsize=12)
ax1.set_ylabel('Station Elevation (m)', fontsize=12)
ax1.grid(True)

# Plot 2: Average Glacier Mass Change by Region
fig2, ax2 = plt.subplots(figsize=(14, 8))
region_mass_change = merged_df.groupby('region')['glacier_mass_change'].mean().sort_values()
region_mass_change.plot(kind='barh', ax=ax2, color='skyblue', edgecolor='black')
ax2.set_title('Average Glacier Mass Change by Region', fontsize=14)
ax2.set_xlabel('Average Mass Change (Gt)', fontsize=12)
ax2.set_ylabel('Region', fontsize=12)
ax2.grid(axis='x', linestyle='--', alpha=0.7)

# Plot 3: Station Elevation vs Glacier Area
fig3, ax3 = plt.subplots(figsize=(12, 8))
ax3.scatter(merged_df['glacier_area'], merged_df['station_elevation'], alpha=0.7, color='green', edgecolors='k', s=80)
ax3.set_title('Station Elevation vs Glacier Area', fontsize=14)
ax3.set_xlabel('Glacier Area (km²)', fontsize=12)
ax3.set_ylabel('Station Elevation (m)', fontsize=12)
ax3.grid(True)

# Display the plots to the user
tools.display_dataframe_to_user(name="Merged Glacier and GTN Data", dataframe=merged_df)
