import {getRoverPath, getAllMissions} from "./getRoverInfo.js";

const params = new URLSearchParams(window.location.search);
const roverName = params.get("name");
const data = await getAllMissions();
let rover;
data.forEach(element => {
    if (element.name == roverName){
        document.querySelector(".name").innerHTML =
        `
            <h1 class="name">
                ${element.name}
            </h1>
        `
        document.querySelector(".left").innerHTML = 
        `
            <div class="inner">
                <h2>Type: ${element.mission_type}</h2>
                <h2>Destination: ${element.celestial_body}</h2>
                <h2>Date of Launch: ${element.launch_year} </h2>
                <h2>Status: ${element.status}</h2>
                <img class="roverImage" src="../img/${element.name}.jpg" alt="">
            </div>
        `
        const moveDiv = document.querySelector(".movement").addEventListener("click", () => {
        window.location.href = `roadMap.html?name=${element.name}`;
        });  
        
        const sensorDiv = document.querySelector(".sensor").addEventListener("click", () => {
        window.location.href = `sensorReadings.html?name=${element.name}`;
        }); 
    }
    else{
        console.log("Rover not Found")
    }
});
