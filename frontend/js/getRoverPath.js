async function getRoverPath(roverName){
    const data = await(await fetch(`http://127.0.0.1:8000/missions/${roverName}/path`)).json();
    console.log(data);
    return data;
}
getRoverPath("Curiosity");