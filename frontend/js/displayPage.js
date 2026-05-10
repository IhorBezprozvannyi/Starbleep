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
                <h2>Type: ${element.type}</h2>
                <h2>Destination: ${element.target}</h2>
                <h2>Date of Launch: ${element.launch_year} </h2>
                <h2>Status: ${element.status}</h2>
                <img class="roverImage" src="../img/${element.name}.jpg" alt="">
            </div>
        `        
    }
    else{
        console.log("Rover not Found")
    }
});

