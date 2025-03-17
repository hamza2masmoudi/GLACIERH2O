#!/bin/bash

# Project name
PROJECT_NAME="glacier-visualization"

# Create base directories
mkdir -p $PROJECT_NAME/{public,src/{components,data},src/styles}

# Create essential files
touch $PROJECT_NAME/public/index.html
touch $PROJECT_NAME/src/{App.jsx,index.js,styles/styles.css}
touch $PROJECT_NAME/src/components/{GlobeVisualization.jsx,RegionDetailChart.jsx,Controls.jsx}
touch $PROJECT_NAME/src/data/{glacier_data.json,gtn_report.json}
touch $PROJECT_NAME/data_preprocessing.py
touch $PROJECT_NAME/package.json

# Add basic content to files
echo "<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Glacier Melt Visualization</title>
</head>
<body>
  <div id='root'></div>
</body>
</html>" > $PROJECT_NAME/public/index.html

echo "import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './styles/styles.css';

ReactDOM.render(<App />, document.getElementById('root'));" > $PROJECT_NAME/src/index.js

echo "{
  \"name\": \"glacier-visualization\",
  \"version\": \"1.0.0\",
  \"scripts\": {
    \"start\": \"react-scripts start\",
    \"build\": \"react-scripts build\"
  },
  \"dependencies\": {
    \"react\": \"^18.0.0\",
    \"react-dom\": \"^18.0.0\",
    \"react-scripts\": \"5.0.1\",
    \"d3\": \"^7.0.0\",
    \"topojson-client\": \"^3.1.0\",
    \"react-chartjs-2\": \"^4.0.0\",
    \"chart.js\": \"^3.5.0\"
  }
}" > $PROJECT_NAME/package.json

echo "# Python script to process data
import zipfile
import pandas as pd
import os
import json

zip_path = 'Glacier.zip'
xlsx_path = 'GTN Report.xlsx'
extract_dir = 'glacier_data'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

glacier_data = []
for file in os.listdir(extract_dir):
    if file.endswith('.csv') and file != '0_global.csv':
        df = pd.read_csv(os.path.join(extract_dir, file))
        region = file.replace('.csv', '')
        for _, row in df.iterrows():
            glacier_data.append({
                \"region\": region,
                \"start_dates\": row['start_dates'],
                \"end_dates\": row['end_dates'],
                \"glacier_area\": row['glacier_area'],
                \"combined_gt\": row['combined_gt'],
                \"combined_mwe\": row['combined_mwe']
            })

with open('src/data/glacier_data.json', 'w') as f:
    json.dump(glacier_data, f, indent=4)

pd.read_excel(xlsx_path).to_json('src/data/gtn_report.json', orient='records', indent=4)
print('✅ Data converted!')" > $PROJECT_NAME/data_preprocessing.py

# Display final structure
echo "✅ Project structure created successfully!"
tree $PROJECT_NAME
