import {getAllMissions} from "./getRoverInfo.js";
import {display} from "./representMars.js";

const placedPositions = []; // keep this outside display()

export function getSpacedPosition(x, y, minDistance = 2) {
  let newX = x;
  let newY = y;
  
  for (const pos of placedPositions) {
    const dx = newX - pos.x;
    const dy = newY - pos.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance < minDistance) {
      // push away from the conflicting position
      newX += dx < 0 ? -minDistance : minDistance;
      newY += dy < 0 ? -minDistance : minDistance;
    }
  }
  
  placedPositions.push({ x: newX, y: newY });
  return [newX, newY];
}

const yearRanges = {
  "2000-2010": { from: 2000, to: 2010 },
  "2010-2020": { from: 2010, to: 2020 },
  "2020-2030": { from: 2020, to: 2030 }
};

async function filter(year, type, status){
    placedPositions.length = 0;
    document.querySelector(".mars").innerHTML = '';
    const data = await getAllMissions();
    console.log(data)
    
    const range = yearRanges[year];
    console.log(range)

    for (const element of data) {
        const missionYear = element.launch_year
        console.log(missionYear)
        const yearMatch = !range || (missionYear >= range.from && missionYear <= range.to);
        console.log(yearMatch)
        const typeMatch = type === "Type" || element.type == type;
        console.log(typeMatch)
        const statusMatch = status === "Status" || element.status == status;
        console.log(statusMatch)
        if (yearMatch && typeMatch && statusMatch){
            await display(element);
        }
    }
}

document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    const year = document.querySelector("#year").value;
    const type = document.querySelector("#type").value;
    const status = document.querySelector("#status").value;

    console.log(year, status, type)

    filter(year, type, status);
});