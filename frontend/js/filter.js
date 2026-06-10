import {getAllMissions} from "./getRoverInfo.js";
import {display} from "./representMars.js";

const placedPositions = []; // keep this outside display()

const filterModal = document.getElementById("filterModal");
const reopenBtn = document.getElementById("reopenFilter");
const mars = document.querySelector(".mars");
const nothing = document.querySelector(".nothing")

mars.classList.add("blurred");


export function getSpacedPosition(x, y, minDistance = 2) {
  let newX = x;
  let newY = y;
  
  for (const pos of placedPositions) {
    const dx = newX - pos.x;
    const dy = newY - pos.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance < minDistance) {
      newX += dx < 0 ? -minDistance : minDistance;
      newY += dy < 0 ? -minDistance : minDistance;
    }
  }
  
  placedPositions.push({ x: newX, y: newY });
  return [newX, newY];
}

const yearRanges = {
  "1990-2000": { from: 1990, to: 2000 },
  "2000-2010": { from: 2000, to: 2010 },
  "2010-2020": { from: 2010, to: 2020 },
  "2020-2030": { from: 2020, to: 2030 }
};

async function filter(year, type, status){
    placedPositions.length = 0;
    document.querySelector(".mars").innerHTML = '';
    const data = await getAllMissions();
    if (!data){
      nothing.classList.remove("hidden");
    }
    console.log(data)
    
    const range = yearRanges[year];
    console.log(range)

    for (const element of data) {
        const missionYear = element.launch_year
        console.log(missionYear)
        const yearMatch = !range || (missionYear >= range.from && missionYear <= range.to);
        console.log(yearMatch)
        const typeMatch = type === "Type" || element.mission_type == type;
        console.log(typeMatch)
        const statusMatch = status === "Status" || element.status == status;
        console.log(statusMatch)
        if (yearMatch && typeMatch && statusMatch){
            await display(element);
        }
    }
    if (mars.innerHTML == ""){
      nothing.classList.remove("hidden");
    }
    else{
      nothing.classList.add("hidden");
    }
}

document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    const year = document.querySelector("#year").value;
    const type = document.querySelector("#type").value;
    const status = document.querySelector("#status").value;

    filterModal.classList.add("hidden");
    mars.classList.remove("blurred");
    reopenBtn.style.display = "block";

    console.log(year, status, type)

    placedPositions.length = 0;
    mars.innerHTML = "";
    filter(year, type, status)
});

reopenBtn.addEventListener("click", () => {
    filterModal.classList.remove("hidden");
    mars.classList.add("blurred");
    reopenBtn.style.display = "none";
    mars.innerHTML = "";
    nothing.classList.add("hidden");
});