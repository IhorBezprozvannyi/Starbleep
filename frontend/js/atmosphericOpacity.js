import {getOpacity} from "./getRoverInfo.js";

const params = new URLSearchParams(window.location.search);
const roverName = params.get("name");

const ctx = document.getElementById('opacityChart').getContext('2d');

const rawData = await getOpacity(roverName);

document.querySelector(".Top").innerHTML = `<h1 class="title">Atmospheric Opacity ${roverName}</h1>`;

function flattenField(data, field) {
    const bySol = {};
    data.forEach(entry => {
        if (entry[field] === null) return; // skip nulls for this field
        const sol = Math.floor(entry.Sol);
        if (!bySol[sol]) bySol[sol] = [];
        bySol[sol].push(entry[field]);
    });

    // average multiple readings per sol
    return Object.entries(bySol).map(([sol, values]) => ({
        sol: Number(sol),
        value: values.reduce((a, b) => a + b, 0) / values.length
    })).sort((a, b) => a.sol - b.sol);
}

let currentField = "tau_440";
let chunkStart = 0;
const chunkSize = 100;

function getChunk(data) {
    return data.filter(d => d.sol >= chunkStart && d.sol < chunkStart + chunkSize);
}

function getSeason(l_s) {
    const normalized = ((l_s % 360) + 360) % 360;
    if (normalized < 90)  return { name: "Spring", color: "#7fbf7f", tempRange: "-60°C to -20°C" };
    if (normalized < 180) return { name: "Summer", color: "#d4b815", tempRange: "-20°C to 20°C" };
    if (normalized < 270) return { name: "Fall",   color: "#c97b3d", tempRange: "-40°C to -10°C" };
    return { name: "Winter", color: "#6f9fd8", tempRange: "-80°C to -60°C" };
}

function buildChart() {
    const flattened = flattenField(rawData.data, currentField);
    const chunk = getChunk(flattened);

    const lsValues = rawData.data
        .filter(d => d.Sol >= chunkStart && d.Sol < chunkStart + chunkSize)
        .map(d => d.l_s);
    const avgLs = lsValues.reduce((a, b) => a + b, 0) / lsValues.length;
    const season = getSeason(avgLs);

    return {
        labels: chunk.map(d => d.sol.toFixed(2)),
        values: chunk.map(d => d.value),
        season
    };
}

const tauChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Optical Depth (τ)',
            data: [],
            borderColor: '#d38a68',
            backgroundColor: 'rgba(211, 138, 104, 0.1)',
            tension: 0.3,
            pointRadius: 3,
            spanGaps: true
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                labels: {
                    color: '#ffffff',
                    font: { size: 20 }
                }
            }
        },
        scales: {
            x: { 
                title: { display: true, text: 'Sol', color: '#ffffff',font: {size: 20}},
                ticks: { color: '#ffffff', font: {size: 16} },
                grid: { color: 'rgba(255,255,255,0.1)' },
            },
            y: {
                title: { display: true, text: 'Optical Depth (τ)', color: '#ffffff',font: {size: 20} },
                ticks: { color: '#ffffff', font: {size: 16} }, 
                grid: { color: 'rgba(255,255,255,0.1)' }
            }
        }
    }
});

function updateChart() {
    const updated = buildChart();
    tauChart.data.labels = updated.labels;
    tauChart.data.datasets[0].data = updated.values;
    tauChart.data.datasets[0].borderColor = updated.season.color;
    tauChart.data.datasets[0].backgroundColor = updated.season.color + "33";
    tauChart.data.datasets[0].label = `Optical Depth (τ) — ${updated.season.name} AvgTemp (${updated.season.tempRange})`;
    tauChart.update();
    document.querySelector("#solRange").textContent = `Sol ${chunkStart}-${chunkStart + chunkSize}`;
}

document.querySelector("#prevChunk").addEventListener("click", () => {
    if (chunkStart > 0) {
        chunkStart -= chunkSize;
        updateChart();
    }
});

document.querySelector("#nextChunk").addEventListener("click", () => {
    chunkStart += chunkSize;
    updateChart();
});

document.querySelector("#tauToggle").addEventListener("change", (e) => {
    currentField = e.target.value;
    updateChart();
});

updateChart();