export async function getRoverPath(roverName){
    const data = await(await fetch(`https://130-61-111-189.sslip.io/missions/${roverName}/path`)).json();
    console.log("getting the path...")
    return data;
}

export async function getAllMissions(){
    const data = await(await fetch(`https://130-61-111-189.sslip.io/missions/all`)).json();
    console.log("getting missions...")
    return data;
}

export async function getPressure(roverName, sol) {
    const data = await(await fetch(`https://130-61-111-189.sslip.io/missions/${roverName}/sensors/${sol}`)).json();
    console.log("getting the pressure...")
    return data;
}

export async function getOpacity(roverName){
    const data = await(await fetch(`https://130-61-111-189.sslip.io/missions/${roverName}/atmospheric_opacity`)).json();
    console.log("getting the opacity...")
    return data;
}

//py -m uvicorn main:app --reload
