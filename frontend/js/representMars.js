import {getRoverPath, getAllMissions} from "./getRoverInfo.js";
import {getSpacedPosition} from "./filter.js"

const data = getAllMissions();
const path = getRoverPath();


function latLonToPercent(lat, lon) {
  const x = (lon + 180) / 360 * 100;
  const yFull = (90 - lat) / 180 * 100;
  const y = yFull * 0.10;
  return [ x, y ];
}

export async function display(element){
    let path = await getRoverPath(element.name);
    console.log("element:", element);
    console.log("path:", path); 
    let coords = path[(path.length) - 1]
    console.log(coords)
    let arr = latLonToPercent(coords.lat, coords.lon);
    console.log(arr);
    let x = arr[0];
    let y = arr[1];
    let [spacedX, spacedY] = getSpacedPosition(x, y, 5);
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