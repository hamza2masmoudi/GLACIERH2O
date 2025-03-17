let chartInstance = null;

export function updateChart(region, darkMode = false) {
  d3.json("data/glacier_data.json").then((data) => {
    // Filter data for the selected region
    const regionData = data
      .filter(d => d.region === region)
      .sort((a, b) => new Date(a.end_date) - new Date(b.end_date));
    
    const ctx = document.getElementById("region-chart").getContext("2d");

    // Destroy existing chart if it exists
    if (chartInstance) {
      chartInstance.destroy();
    }

    // Determine text and grid colors based on dark mode
    const textColor = darkMode ? "#ecf0f1" : "#34495e";
    const gridColor = darkMode ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 0, 0, 0.1)";

    // Chart options
    const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: textColor
          }
        },
        title: {
          display: true,
          text: region === 'global' ? 'Global Glacier Mass Change' : `${region.replace(/_/g, ' ')} Glacier Mass Change`,
          font: {
            size: 14
          },
          color: textColor
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Year",
            color: textColor
          },
          ticks: {
            color: textColor
          },
          grid: {
            color: gridColor
          }
        },
        y: {
          title: {
            display: true,
            text: "Mass Change (Gt)",
            color: textColor
          },
          ticks: {
            color: textColor
          },
          grid: {
            color: gridColor
          }
        }
      }
    };

    // Create the chart
    chartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: regionData.map(d => d.end_date),
        datasets: [{
          label: region === 'global' ? "Global Glacier Mass Change" : `${region.replace(/_/g, ' ')} Glacier Mass Change`,
          data: regionData.map(d => d.glacier_mass_change),
          borderColor: "#3498db",
          backgroundColor: "rgba(52, 152, 219, 0.2)",
          fill: true,
          tension: 0.4,
          pointRadius: 3,
          pointBackgroundColor: "#3498db"
        }]
      },
      options: options
    });
  });
}

export { chartInstance };