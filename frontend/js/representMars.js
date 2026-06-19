import {getRoverPath, getAllMissions} from "./getRoverInfo.js";
import {getSpacedPosition} from "./filter.js"
import { latLonToPercent } from "./latLonToPercent.js";



const data = getAllMissions();
const path = getRoverPath();

const MISSION_POSITIONS = {
    "Perseverance": { x: 70, y: 35 },
    "Curiosity":    { x: 80, y: 50},
    "Opportunity":  { x: 50, y: 45 },
    "Spirit":       { x: 95, y: 55 },
};

export async function display(element){
    
    const pos = MISSION_POSITIONS[element.name];
    if (!pos) {
        console.warn("No position defined for", element.name);
        return;
    }

    console.log("element:", element);

    const [spacedX, spacedY] = getSpacedPosition(pos.x, pos.y, 5);
    
    const div = document.createElement("div");
    div.className = "icon-wrapper";
    div.dataset.name = element.name;
    div.style = `position: absolute; left: ${spacedX}%; top: ${spacedY}%; cursor: pointer;`;
    div.innerHTML = `<img class="machine" src="../img/place.svg" style="width: 5vw; height: 5vw; filter: invert();">`;

    div.addEventListener("click", () => {
        window.location.href = `displayMachine.html?name=${element.name}`;
    });

    document.querySelector(".mars").appendChild(div);
}