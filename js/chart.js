let chartInstance = null;

export function updateChart(region, darkMode = false) {
  d3.json("data/glacier_data.json").then((data) => {
    const regionData = data.filter(d => d.region === region).sort((a, b) => new Date(a.end_date) - new Date(b.end_date));
    const globalData = data.sort((a, b) => new Date(a.end_date) - new Date(b.end_date));

    const ctx1 = document.getElementById("region-chart-1").getContext("2d");
    const ctx2 = document.getElementById("region-chart-2").getContext("2d");

    // Destroy existing charts
    if (chartInstance) chartInstance.forEach(chart => chart.destroy());

    const textColor = darkMode ? "#ecf0f1" : "#34495e";
    const gridColor = darkMode ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 0, 0, 0.1)";

    const commonOptions = {
      responsive: true,
      plugins: {
        legend: { labels: { color: textColor } },
      },
      scales: {
        x: { title: { display: true, text: "Year", color: textColor }, ticks: { color: textColor }, grid: { color: gridColor } },
        y: { title: { display: true, text: "Mass Change (Gt)", color: textColor }, ticks: { color: textColor }, grid: { color: gridColor } },
      },
    };

    // Chart 1: Glacier Mass Change Over Time
    const chart1 = new Chart(ctx1, {
      type: "line",
      data: {
        labels: regionData.map(d => d.end_date),
        datasets: [{
          label: "Glacier Mass Change (Gt)",
          data: regionData.map(d => d.glacier_mass_change),
          borderColor: "#3498db",
          backgroundColor: "rgba(52, 152, 219, 0.2)",
          fill: true,
          tension: 0.4,
        }],
      },
      options: commonOptions,
    });

    // Chart 2: Global Area vs. Mass Change
    const chart2 = new Chart(ctx2, {
      type: "scatter",
      data: {
        datasets: [{
          label: "Global Area vs. Mass Change",
          data: globalData.map(d => ({ x: d.glacier_area, y: d.glacier_mass_change })),
          backgroundColor: "rgba(46, 204, 113, 0.5)",
          pointRadius: 6,
        }],
      },
      options: {
        ...commonOptions,
        scales: {
          x: { title: { display: true, text: "Glacier Area (km²)", color: textColor }, ticks: { color: textColor }, grid: { color: gridColor } },
          y: { title: { display: true, text: "Mass Change (Gt)", color: textColor }, ticks: { color: textColor }, grid: { color: gridColor } },
        },
      },
    });

    chartInstance = [chart1, chart2];
  });
}
