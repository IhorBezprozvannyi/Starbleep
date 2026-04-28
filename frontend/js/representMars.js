import {getRoverPath, getAllMissions} from "./getRoverInfo.js";

const data = getAllMissions();
const path = getRoverPath();


function latLonToPercent(lat, lon) {
  const x = (lon + 180) / 360 * 100;
  const yFull = (90 - lat) / 180 * 100;
  const y = yFull * 0.20;
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
    let lon = arr[0];
    let lat = arr[1];
    document.querySelector(".mars").innerHTML += `
        <img class="machine" src="../img/place.svg" style="position: absolute; left: ${lon}%; top: ${lat}%; width: 4vw; height: 4vw; transform: rotate(45deg)">
    `
}