import { updateChart, chartInstance } from "./chart.js";

document.addEventListener("DOMContentLoaded", () => {
  const yearSlider = document.getElementById("year-slider");
  const yearInput = document.getElementById("year-input");
  const baseMapSelector = document.getElementById("basemap-select");
  const darkModeToggle = document.getElementById("dark-mode-toggle");

  let glacierData = [];
  let currentRegion = 'global'; // Default to global view

  // Initialize the map
  const map = L.map("map").setView([20, 0], 2);

  // Define base map layers
  const baseMaps = {
    "OpenStreetMap": L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"),
    "Satellite": L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")
  };

  // Add initial base layer
  let currentBaseLayer = baseMaps["OpenStreetMap"];
  currentBaseLayer.addTo(map);

  // Handle base map selection
  baseMapSelector.addEventListener("change", (e) => {
    map.removeLayer(currentBaseLayer);
    currentBaseLayer = baseMaps[e.target.value];
    currentBaseLayer.addTo(map);
  });

  // Create legend for map
  const createLegend = () => {
    const legend = L.control({ position: "topright" });

    legend.onAdd = () => {
      const div = L.DomUtil.create("div", "info legend");
      div.setAttribute("id", "legend");
      div.innerHTML = `
        <div class="legend-title">Glacier Mass Change</div>
        <div class="legend-item">
          <div class="color-box" style="background-color: #003366;"></div>
          <span>Freeze (&ge; 10 Gt)</span>
        </div>
        <div class="legend-item">
          <div class="color-box" style="background-color: #33cc33;"></div>
          <span>Stable (-10 to 10 Gt)</span>
        </div>
        <div class="legend-item">
          <div class="color-box" style="background-color: #ff3300;"></div>
          <span>Melting (&lt; -10 Gt)</span>
        </div>
      `;

      // Prevent map interactions when clicking on legend
      L.DomEvent.disableClickPropagation(div);
      return div;
    };

    legend.addTo(map);
  };

  // Update map markers based on selected year
  const updateMapMarkers = (year) => {
    // Clear existing markers
    map.eachLayer(layer => {
      if (layer instanceof L.CircleMarker) {
        map.removeLayer(layer);
      }
    });

    // Add new markers for the selected year
    glacierData
      .filter(d => Math.round(d.end_date) === +year)
      .forEach((data) => {
        // Determine color based on mass change
        let fillColor;
        if (data.glacier_mass_change >= 10) {
          fillColor = "#003366"; // Freeze
        } else if (data.glacier_mass_change <= -10) {
          fillColor = "#ff3300"; // Melting
        } else {
          fillColor = "#33cc33"; // Stable
        }

        // Create circle marker
        const marker = L.circleMarker([data.latitude, data.longitude], {
          radius: Math.max(data.glacier_area / 2000, 6),
          fillColor,
          color: "#222",
          weight: 1,
          fillOpacity: 0.8
        });

        // Add popup with region information
        marker.bindPopup(`
          <strong>Region:</strong> ${data.region.replace(/_/g, " ")}<br>
          <strong>Mass Change:</strong> ${data.glacier_mass_change} Gt
        `);

        // Add click event to update charts
        marker.on('click', function() {
          currentRegion = data.region;
          updateChart(data.region, document.body.classList.contains('dark-mode'));
        });

        // Add marker to map
        marker.addTo(map);
      });
  };

  // Handle year slider input
  yearSlider.addEventListener("input", (e) => {
    yearInput.value = e.target.value;
    updateMapMarkers(e.target.value);
  });

  // Handle year input changes
  yearInput.addEventListener("input", (e) => {
    const year = Math.max(2000, Math.min(2025, e.target.value));
    yearSlider.value = year;
    updateMapMarkers(year);
  });

  // Toggle dark mode
  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    darkModeToggle.textContent = document.body.classList.contains("dark-mode") 
      ? "☀️ Light Mode" 
      : "🌙 Dark Mode";
    
    // Update charts with new theme
    updateChart(currentRegion, document.body.classList.contains('dark-mode'));
  });

  // Add window resize handler
  window.addEventListener('resize', () => {
    if (chartInstance) {
      chartInstance.resize();
    }
  });

  // Initialize the application
  Promise.all([
    d3.json("data/glacier_data.json")
  ]).then(([data]) => {
    glacierData = data;
    updateMapMarkers(yearSlider.value);
    createLegend();
    updateChart('global', document.body.classList.contains('dark-mode'));
  }).catch(error => {
    console.error("Error loading data:", error);
  });
});