import {getAllMissions} from "./getRoverInfo.js";
import {display} from "./representMars.js";

async function filter(year, type, status){
    const data = await getAllMissions();
    console.log(data)
    data.forEach(element => {
        if (element.type == type && element.status == status){
            console.log(element)
            display(element);
        }
    });
}

document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    const year = document.querySelector("#year").value;
    const type = document.querySelector("#type").value;
    const status = document.querySelector("#status").value;

    console.log(year, status, type)

    filter(year, type, status);
});