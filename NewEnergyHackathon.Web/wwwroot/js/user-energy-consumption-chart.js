﻿fetch('/daily-green-consumption?dateTo=2025-03-23&dateFrom=2025-03-21')
	.then(response => response.json())
	.then(wrapper => {
		const dataset = wrapper.data;

		const labels = dataset.map((item) => {
			const asDate = new Date(item.items_Timestamp_UTC);

			return `${String(asDate.getUTCHours()).padStart(2, '0')}:${String(asDate.getUTCMinutes()).padStart(2, '0')}`;
		});
		const greenData = dataset.map(entry => entry.consumptionDeliveryTotal_Green / 1000);
		const nonGreenData = dataset.map(entry => entry.consumptionDeliveryTotal_NoGreen / 1000);

		const ctx = document.getElementById('userConsumptionChart').getContext('2d');
		new Chart(ctx, {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [
					{
						label: 'Groen',
						data: greenData,
						backgroundColor: 'rgba(0, 255, 0, 0.5)',
						borderColor: 'rgba(0, 255, 0, 0.5)',
						borderWidth: 1
					},
					{
						label: 'Niet groen',
						data: nonGreenData,
						backgroundColor: 'rgba(99, 102, 106, 0.5)',
						borderColor: 'rgba(99, 102, 106, 0.5)',
						borderWidth: 1
					}
				]
			},
			options: {
				responsive: true,
				scales: {
					xAxes: [{
						stacked: true,
						scaleLabel: {
							display: true,
							labelString: 'Tijdstip',
							fontSize: 14,
							fontStyle: 'bold'
						}
					}],
					yAxes: [{
						stacked: true,
						scaleLabel: {
							display: true,
							labelString: 'Verbruik (kWh)',
							fontSize: 14,
							fontStyle: 'bold'
						},
					}]
				},
				tooltips: {
					mode: 'index',
					intersect: false,
					callbacks: {
						label: function (tooltipItem, data) {
							const dataset = data.datasets[tooltipItem.datasetIndex];
							const value = dataset.data[tooltipItem.index];
							return `${dataset.label}: ${Math.round(value)} kWh`;
						}
					}
				},
				plugins: {
					legend: {
						position: 'top'
					}
				}
			}
		});
	})
	.catch(error => console.error('Error loading chart data:', error));