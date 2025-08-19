export default async function dashboardStat() {
    const { default: ApexCharts } = await import("apexcharts");
    const usageChartData = JSON.parse(document.getElementById('usageChartData').textContent);
    const topEndpointsChartData = JSON.parse(document.getElementById('topEndpointsChartData').textContent);
    if (!usageChartData || !topEndpointsChartData) return;

    // Usage Chart
    const apiUsageId = document.querySelector("#usageChart");
    if (apiUsageId) {
        let usageChart = new ApexCharts(apiUsageId, {
            chart: { type: 'line', height: 300 },
            stroke: { width: 2, curve: 'smooth' },
            series: [
                { name: 'Total Requests', data: usageChartData.total },
                { name: 'Success', data: usageChartData.success },
                { name: 'Errors', data: usageChartData.errors }
            ],
            xaxis: {
                categories: usageChartData.dates.map((date, i) => `${usageChartData.api[i]} (${date})`),
                title: { text: "API / Date" }
            },
            yaxis: {
                title: { text: "Requests" }
            },
            markers: { size: 4 },
            colors: ['#008FFB', '#00E396', '#FF4560'],
            tooltip: {
                shared: true,
                intersect: false,
            }
        });
        usageChart.render();
    }

    // Endpoints Chart
    const topEndpointId = document.querySelector("#endpointsChart");
    if (topEndpointId) {
        let chart = new ApexCharts(topEndpointId, {
            chart: { type: 'bar', height: 300 },
            plotOptions: { bar: { horizontal: true } },
            series: [{
                name: 'Requests',
                data: topEndpointsChartData.counts
            }],
            xaxis: { categories: topEndpointsChartData.resources }
        });
        chart.render();
    }
}
