import { getPressure } from "./getRoverInfo.js";

const params = new URLSearchParams(window.location.search);
const roverName = params.get("name");

const top = document.querySelector(".Top");
top.innerHTML = `<h1 class="title">${roverName} Sensor Readings</h1>`;

let currentSol = 1;

const ctx = document.getElementById('pressureChart').getContext('2d');

const pressureChart = new Chart(ctx, { 
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Pressure (Pa)',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.4,
            pointRadius: 3,
        }]
    },
    options: {
        responsive: true,
        scales: {
        x: {
            title: { display: true, text: 'Time (LTST)', color: '#ffffff',font: {size: 12}},
            ticks: { color: '#ffffff' },
            grid: { color: 'rgba(255,255,255,0.1)' },
        },
        y: {
            title: { display: true, text: 'Pressure (Pa)', color: '#ffffff',font: {size: 12} },
            ticks: { color: '#ffffff' }, 
            grid: { color: 'rgba(255,255,255,0.1)' },
            font: {
                size: 12
            }
        }
        }
    }
});

async function updateChart(sol) {
    const result = await getPressure(roverName, sol);
    const data = result.timeline;
    document.querySelector("#sol").textContent = `Sol ${sol}`;
    pressureChart.data.labels = data.map(r => r.ltst.split(" ")[1]);
    pressureChart.data.datasets[0].data = data.map(r => r.pressure);
    pressureChart.update();
}


document.querySelector("#prevSol").addEventListener("click", () => {
    if (currentSol > 0) {
        currentSol--;
        updateChart(currentSol);
    }
});

document.querySelector("#nextSol").addEventListener("click", () => {
        currentSol++;
        updateChart(currentSol);
});

updateChart(currentSol);