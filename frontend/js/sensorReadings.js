import { getPressure } from "./getRoverInfo.js";

const params = new URLSearchParams(window.location.search);
const roverName = params.get("name");

const top = document.querySelector(".Top");
top.innerHTML = `<h1>${roverName} Sensor Readings</h1>`;

let currentSol = 1;

const sols = Object.keys(bySol).map(Number).sort((a, b) => a - b);

const ctx = document.getElementById('pressureChart').getContext('2d');

const pressureChart = new Chart(ctx, { 
    type: 'line',
    data: {
        labels: bySol[currentSol].map(reading => reading.ltst.split(" ")[1]),
        datasets: [{
            label: 'Pressure (Pa)',
            data: bySol[currentSol].map(reading => reading.pressure),
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.4,
            pointRadius: 3,
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {title: {display: true, text: 'Time (LTST)'}},
            y: {title: {display: true, text: 'Pressure (Pa)'}}
        }
    }
});

function updateChart(sol){
    const data = getPressure(roverName, sol);
    document.querySelector("#sol").textContent = sol;
    pressureChart.data.labels = bySol[currentSol].map(reading => reading.ltst.split(" ")[1]);
    pressureChart.data.datasets[0].data = bySol[currentSol].map(reading => reading.pressure);
    pressureChart.update();
}

document.querySelector("#prevSol").addEventListener("click", () => {
    if (currentSol > 0) {
        currentSol--;
        updateChart(currentSol);
    }
});

document.querySelector("#nextSol").addEventListener("click", () => {
    if (currentSol < sols.length - 1) {
        currentSol++;
        updateChart(currentSol);
    }
});

updateChart(currentSol);