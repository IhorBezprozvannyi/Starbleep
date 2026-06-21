import { getRoverPath } from "./getRoverInfo.js";

const params = new URLSearchParams(window.location.search);
const roverName = params.get("name");
const path = await getRoverPath(roverName);
path.sort((a, b) => new Date(a.earth_date) - new Date(b.earth_date));

document.getElementById('name').innerText = roverName;

const lats = path.map(p => p.lat);
const lons = path.map(p => p.lon);
const minLat = Math.min(...lats), maxLat = Math.max(...lats);
const minLon = Math.min(...lons), maxLon = Math.max(...lons);

const offsetX = 50, offsetY = 50, scaleX = 900, scaleY = 400;
const svg = document.querySelector(".map");
svg.setAttribute("viewBox", "0 0 1000 500");

const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
defs.innerHTML = `<marker id="arrow" markerWidth="6" markerHeight="6" refX="6" refY="3" orient="auto">
                    <path d="M0,0 L0,6 L6,3 z" fill="#ffffff"/>
                  </marker>`;
svg.appendChild(defs);

function updateInfoCards(point) {
    document.getElementById('display-distance').innerText = (point.total_distance_km || 0) + " km";
    document.getElementById('display-date').innerText = point.earth_date;
    document.getElementById('display-photos').innerText = point.photos_taken || 0;
}

function drawPath(start) {
    while (svg.lastChild !== defs) { svg.removeChild(svg.lastChild); }

    const slice = path.slice(start, start + 10);

    slice.forEach((point, index) => {
        const x = offsetX + (point.lon - minLon) / (maxLon - minLon || 1) * scaleX;
        const y = offsetY + (point.lat - minLat) / (maxLat - minLat || 1) * scaleY;

        if (index > 0) {
            const prev = slice[index - 1];
            const px = offsetX + (prev.lon - minLon) / (maxLon - minLon || 1) * scaleX;
            const py = offsetY + (prev.lat - minLat) / (maxLat - minLat || 1) * scaleY;
            
            const r = 15; // dot radius
            const angle = Math.atan2(y - py, x - px);

            const x1 = px + Math.cos(angle) * r; // start at edge of source dot
            const y1 = py + Math.sin(angle) * r;
            const x2 = x - Math.cos(angle) * r;  // end at edge of target dot
            const y2 = y - Math.sin(angle) * r;


            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", x1); line.setAttribute("y1", y1);
            line.setAttribute("x2", x2); line.setAttribute("y2", y2);
            line.setAttribute("stroke", "#ffffff7f");
            line.setAttribute("stroke-width", "4");
            line.setAttribute("marker-end", "url(#arrow)");
            svg.appendChild(line);
        }

        const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        dot.setAttribute("cx", x); dot.setAttribute("cy", y);
        dot.setAttribute("r", "15");
        dot.setAttribute("class", "dot");
        dot.setAttribute("fill", index === 0 ? "#19a700" : "#ffffff");
        if(index == 9) dot.setAttribute("fill", "#0072a7");
        
        dot.style.cursor = "pointer";
        dot.addEventListener("click", () => updateInfoCards(point));
        svg.appendChild(dot);
    });
}

let start = 0;
document.querySelector("#left").addEventListener("click", () => {
    if (start > 0) { start -= 10; drawPath(start); document.querySelector("#num").innerHTML = start; }
});
document.querySelector("#right").addEventListener("click", () => {
    if (start < path.length - 10) { start += 10; drawPath(start); document.querySelector("#num").innerHTML = start; }
});

drawPath(start);

async function downloadFullJSON() {
    const blob = new Blob([JSON.stringify(path, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${roverName}_Rover_Movement.json`;
    link.click();
}

document.querySelector("#downloadFullJSON").addEventListener("click", downloadFullJSON);