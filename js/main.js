import { updateChart } from "./chart.js";

document.addEventListener("DOMContentLoaded", () => {
  const yearSlider = document.getElementById("year-slider");
  const yearInput = document.getElementById("year-input");
  const baseMapSelector = document.getElementById("basemap-select");
  const darkModeToggle = document.getElementById("dark-mode-toggle");

  let glacierData = [];

  const isDarkMode = () => document.body.classList.contains("dark-mode");

  // Dark mode toggle
  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    darkModeToggle.textContent = isDarkMode() ? "☀️ Light Mode" : "🌙 Dark Mode";
    updateChart(currentRegion, isDarkMode());
  });

  const map = L.map("map").setView([20, 0], 2);
  const baseMaps = {
    "OpenStreetMap": L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"),
    "Satellite": L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"),
    "Terrain": L.tileLayer("https://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg"),
  };
  baseMaps["OpenStreetMap"].addTo(map);

  baseMapSelector.addEventListener("change", (e) => {
    Object.values(baseMaps).forEach(layer => map.removeLayer(layer));
    baseMaps[e.target.value].addTo(map);
  });

  const updateMapMarkers = (year) => {
    map.eachLayer(layer => {
      if (layer instanceof L.CircleMarker) map.removeLayer(layer);
    });

    glacierData.filter(d => Math.round(d.end_date) === +year).forEach((data) => {
      L.circleMarker([data.latitude, data.longitude], {
        radius: Math.max(data.glacier_area / 2000, 6),
        fillColor: data.glacier_mass_change > -10 && data.glacier_mass_change < 10 ? "#33cc33" : d3.scaleSequential(d3.interpolateRdYlBu).domain([-100, 100])(data.glacier_mass_change),
        color: "#222",
        weight: 1,
        fillOpacity: 0.8,
      })
      .bindPopup(`<strong>Region:</strong> ${data.region.replace(/_/g, " ")}<br><strong>Mass Change:</strong> ${data.glacier_mass_change} Gt`)
      .on("click", () => updateChart(data.region, isDarkMode()))
      .addTo(map);
    });
  };

  yearSlider.addEventListener("input", (e) => {
    yearInput.value = e.target.value;
    updateMapMarkers(e.target.value);
  });

  yearInput.addEventListener("input", (e) => {
    const year = Math.max(2000, Math.min(2025, e.target.value));
    yearSlider.value = year;
    updateMapMarkers(year);
  });

  d3.json("data/glacier_data.json").then((data) => {
    glacierData = data;
    updateMapMarkers(yearSlider.value);
  });
});
