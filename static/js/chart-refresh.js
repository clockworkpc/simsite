let chart;

async function fetchChartData() {
  const response = await fetch("/chart-data");
  return await response.json();
}

async function renderChart() {
  const data = await fetchChartData();
  const ctx = document.getElementById('progressChart').getContext('2d');

  if (chart) {
    chart.data.labels = data.labels;
    chart.data.datasets = data.datasets;
    chart.update();
  } else {
    chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: data.datasets
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' },
          title: { display: true, text: 'SimSite Metrics Over Time' }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }
}

setInterval(renderChart, 3000);
document.addEventListener("DOMContentLoaded", renderChart);
