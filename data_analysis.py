import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the glacier data (assumed to be preloaded)
region_data = pd.read_csv('glacier_data/1_alaska.csv')  # Example file, adjust as necessary

# Load the GTN dataset
gtn_data = pd.read_excel('GTN Report.xlsx')  # Example for GTN data

# Set the plot style
sns.set(style="whitegrid")

# Create a figure with 3 subplots
fig, axes = plt.subplots(3, 1, figsize=(10, 18))
fig.suptitle('Glacier and River Discharge Visualization Prototype', fontsize=16)

# 1. Time-based Change (Glacier Mass Change Over Time)
axes[0].plot(region_data['end_dates'], region_data['combined_gt'], marker='o', color='b', label='Mass Change (Gt)')
axes[0].set_title('Glacier Mass Change Over Time', fontsize=14)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Mass Change (Gt)')
axes[0].legend()

# 2. Size-based Relationship (Glacier Area vs. Glacier Mass Change)
axes[1].scatter(region_data['glacier_area'], region_data['combined_gt'], c=region_data['end_dates'], cmap='viridis')
axes[1].set_title('Glacier Area vs. Mass Change', fontsize=14)
axes[1].set_xlabel('Glacier Area (km²)')
axes[1].set_ylabel('Mass Change (Gt)')
cbar = fig.colorbar(plt.cm.ScalarMappable(cmap='viridis'), ax=axes[1])
cbar.set_label('Year')

# 3. Scatter Plot: Glacier Mass Change vs. Catchment Size (Matching regions and years)
# Filter data for matching years and regions (for Alaska in this case)
region_name = 'alaska'
catchment_data = gtn_data[gtn_data['river_name'].str.contains(region_name, case=False, na=False)]  # Adjust for region

# Merge datasets based on year (assuming region_data and catchment_data are aligned)
merged_data = pd.merge(region_data, catchment_data, left_on='end_dates', right_on='station_elevation', how='inner')

# Ensure both datasets have matching rows
if not merged_data.empty:
    axes[2].scatter(merged_data['CATCHMENT_SIZE'], merged_data['combined_gt'], color='r', alpha=0.5)
    axes[2].set_title('Glacier Mass Change vs. Catchment Size', fontsize=14)
    axes[2].set_xlabel('Catchment Size (km²)')
    axes[2].set_ylabel('Mass Change (Gt)')
else:
    axes[2].text(0.5, 0.5, 'No matching data for selected region', ha='center', va='center', fontsize=12, color='red')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()
