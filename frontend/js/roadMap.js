import { getRoverPath } from "./getRoverInfo.js";

const params = new URLSearchParams(window.location.search);
const roverName = params.get("name");
const path = await getRoverPath(roverName);

const offsetX = 50, offsetY = 50;
const scaleX = 900, scaleY = 400;

function toSVG(lat, lon) {
    const x = offsetX + (lon - minLon) / (maxLon - minLon) * scaleX;
    const y = offsetY + (lat - minLat) / (maxLat - minLat) * scaleY;
    return [x, y];
}

const svg = document.querySelector(".map");
svg.setAttribute("viewBox", "0 0 1000 500");
svg.setAttribute("preserveAspectRatio", "xMidYMid meet");

const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
const marker = document.createElementNS("http://www.w3.org/2000/svg", "marker");
marker.setAttribute("id", "arrow");
marker.setAttribute("markerWidth", "6");
marker.setAttribute("markerHeight", "6");
marker.setAttribute("refX", "6");
marker.setAttribute("refY", "3");
marker.setAttribute("orient", "auto");

const arrowHead = document.createElementNS("http://www.w3.org/2000/svg", "path");
arrowHead.setAttribute("d", "M0,0 L0,6 L6,3 z");
arrowHead.setAttribute("fill", "#ffffff");
marker.appendChild(arrowHead);
defs.appendChild(marker);

path.sort((a, b) => new Date(a.earth_date) - new Date(b.earth_date));

function drawPath(start) {
    svg.innerHTML = ""; // clear previous drawing
    svg.appendChild(defs); // re-add the arrow marker

    const slice = path.slice(start, start + 10);

    // 👇 calculate min/max from the slice, not the full path
    const lats = slice.map(p => p.lat);
    const lons = slice.map(p => p.lon);
    const minLat = Math.min(...lats), maxLat = Math.max(...lats);
    const minLon = Math.min(...lons), maxLon = Math.max(...lons);

    slice.forEach((point, index) => {
        const x = offsetX + (point.lon - minLon) / (maxLon - minLon) * scaleX;
        const y = offsetY + (point.lat - minLat) / (maxLat - minLat) * scaleY;

        if (index > 0) {
            const prevX = offsetX + (slice[index-1].lon - minLon) / (maxLon - minLon) * scaleX;
            const prevY = offsetY + (slice[index-1].lat - minLat) / (maxLat - minLat) * scaleY;
            const angle = Math.atan2(y - prevY, x - prevX);
            const r = 15;

            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", prevX + Math.cos(angle) * r);
            line.setAttribute("y1", prevY + Math.sin(angle) * r);
            line.setAttribute("x2", x - Math.cos(angle) * r);
            line.setAttribute("y2", y - Math.sin(angle) * r);
            line.setAttribute("stroke", "#ffffff7f");
            line.setAttribute("stroke-width", "4");
            line.setAttribute("marker-end", "url(#arrow)");
            svg.appendChild(line);
        }

        const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        dot.setAttribute("cx", x);
        dot.setAttribute("cy", y);
        dot.setAttribute("r", "15");
        dot.setAttribute("fill", index === 0 ? "#19a700" : "#ffffff");
        if(index == 9){
            dot.setAttribute("fill", "#0072a7");
        }
        svg.appendChild(dot);
    });
}

const prev = document.querySelector("#left");
const next = document.querySelector("#right");

let start = 0;

document.querySelector("#num").innerHTML = start;

function clickPrev(){
        console.log("prev")
    if (start > 0){
        start -= 10;
    }
    document.querySelector("#num").innerHTML = start;
    drawPath(start);
}

prev.addEventListener("click", () => clickPrev(start));

function clickNext(point){
    console.log("next")
    if (start < path.length - 10){
        start += 10;
    }
    document.querySelector("#num").innerHTML = start;
    drawPath(start);
}

next.addEventListener("click", () => clickNext(start));
drawPath(start);