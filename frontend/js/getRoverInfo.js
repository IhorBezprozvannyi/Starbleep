export async function getRoverPath(roverName){
    const data = await(await fetch(`http://127.0.0.1:8000/missions/${roverName}/path`)).json();
    console.log("getting the path...")
    return data;
}

export async function getAllMissions(){
    const data = await(await fetch(`http://127.0.0.1:8000/missions/all`)).json();
    console.log("getting missions...")
    return data;
}

export async function getPressure(roverName, sol) {
    const data = await(await fetch(`http://127.0.0.1:8000/missions/${roverName}/sensors/${sol}`)).json();
    console.log("getting the pressure...")
    return data;
}

//py -m uvicorn main:app --reload
