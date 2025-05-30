﻿const greenTips = [
	"Duurzame energie? Kies het juiste moment!<br><br>Tussen 13:00 en 15:00 uur draait Nederland op groene stroom. Tip: laat de kinderen hun tablets opladen of zet alvast de was aan. Zo leert het hele gezin bewuster omgaan met energie – zonder moeite!",
	"Groenste uren vandaag: 14:15 – 16:30 uur<br><br>In deze periode komt >85% van de stroom uit zon en wind. Plan slim: stel je was uit tot vanmiddag, laad je laptop op of start een warm programma in de vaatwasser. Kleine keuzes, groot effect.",
	"Help het net én het klimaat<br><br>Vandaag is er veel groene stroom beschikbaar tussen 11:30 en 14:00 uur. Door je apparaten in deze periode te gebruiken, verlaag je jouw CO₂-voetafdruk en help je mee om het stroomnet in balans te houden. Denk aan je vaatwasser, elektrische fiets opladen of het voorverwarmen van je oven.",
	"Gebruik stroom wanneer deze het duurzaamst is<br><br>Tussen 12:45 en 15:00 uur is het aandeel zonne- en windenergie op zijn hoogst. Zet in dit tijdvak energie-intensieve apparaten aan zoals je wasmachine, droger of laadpaal. Zo benut je maximaal de groene stroom van vandaag."
];

function displayRandomTip() {
	const randomIndex = Math.floor(Math.random() * greenTips.length);
	document.getElementById('greenEnergyTip').innerHTML = greenTips[randomIndex];
}

function formatDate(date) {
	return date.toISOString().split('T')[0];
}

function navigateTo(date) {
	const formattedDate = formatDate(date);
	window.location.href = `/Home/GreenEnergyForecast?dateTo=${formattedDate}&dateFrom=${formattedDate}`;
}

function buildGraph(data) {
	Chart.defaults.global.defaultFontFamily = 'Nunito';
	Chart.defaults.global.defaultFontColor = '#858796';

	const ctx = document.getElementById("forecastChart").getContext('2d');

	new Chart(ctx, {
		type: 'bar',
		data: {
			labels: data.map((input) => {
				const date = new Date(input.validfrom);
				return `${String(date.getUTCHours()).padStart(2, '0')}:${String(date.getUTCMinutes()).padStart(2, '0')}`;
			}),
			datasets: [
				{
					label: 'Wind',
					data: data.map((input) => input.Wind_Percentage ?? input.wind_Percentage ?? 0),
					backgroundColor: '#82b9ea',
					stack: 'combined'
				},
				{
					label: 'Zon',
					data: data.map((input) => input.Solar_Percentage ?? input.solar_Percentage ?? 0),
					backgroundColor: '#f9c951',
					stack: 'combined'
				}
			]
		},
		options: {
			responsive: true,
			tooltips: {
				mode: 'index',
				intersect: false,
				callbacks: {
					label: function (tooltipItem, data) {
						const dataset = data.datasets[tooltipItem.datasetIndex];
						return `${dataset.label}: ${Math.round(dataset.data[tooltipItem.index])}%`;
					}
				}
			},
			legend: { position: 'bottom' },
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
						labelString: 'Percentage',
						fontSize: 14,
						fontStyle: 'bold'
					},
					ticks: {
						beginAtZero: true,
						max: 100,
						stepSize: 10
					}
				}]
			}
		}
	});
}

function buildGraphWithScore(data, score) {
	buildGraph(data);
	const roundedScore = score?.toFixed(1) ?? "0.0";
	document.getElementById("score1").textContent = `${roundedScore}%`;
	document.getElementById("explanation1").textContent = `Op deze dag was ${roundedScore}% van alle energie op het net groen.`;
}

document.addEventListener("DOMContentLoaded", function () {
	displayRandomTip();

	const dateInput = document.getElementById('selectedDate');
	const urlParams = new URLSearchParams(window.location.search);
	const beforeParam = urlParams.get('dateFrom');
	const defaultDate = new Date('2025-03-22');
	const selected = beforeParam ? new Date(beforeParam) : defaultDate;
	const selectedDateStr = formatDate(selected);
	dateInput.value = selectedDateStr;

	fetch(`/daily-green-energy?dateTo=${selectedDateStr}&dateFrom=${selectedDateStr}`)
		.then(res => res.json())
		.then(result => {
			const data = result.data;
			const score = result.dailyGreenScoreGrid;
			if (!Array.isArray(data)) {
				console.error("Expected 'data' to be an array:", data);
				return;
			}
			buildGraphWithScore(data, score);
		})
		.catch(err => console.error("Fetch or render error:", err));

	document.getElementById('prevDay').addEventListener('click', function () {
		const newDate = new Date(dateInput.value);
		newDate.setDate(newDate.getDate() - 1);
		navigateTo(newDate);
	});

	document.getElementById('nextDay').addEventListener('click', function () {
		const newDate = new Date(dateInput.value);
		newDate.setDate(newDate.getDate() + 1);
		navigateTo(newDate);
	});

	dateInput.addEventListener('change', function () {
		navigateTo(new Date(this.value));
	});
});