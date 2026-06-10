
function animateNumber(element, target, duration = 1500) {
    let start = 0;
    const increment = target / (duration / 35); // 16ms per frame (~60fps)
    
    const timer = setInterval(() => {
        start += increment;
        if (Math.floor(start).toString().length == 1){
            element.textContent = "0" + String(Math.floor(start));
            console.log(element.textContent)
        }
        else{
            element.textContent = Math.floor(start);
        }

        
        if (start >= target) {
            element.textContent = target; // make sure it lands exactly on target
            clearInterval(timer);
        }
    }, 16);
}
const counter = document.querySelectorAll(".missionCount");
console.log(counter[0].innerHTML)
animateNumber(counter[0], counter[0].innerHTML);
animateNumber(counter[1], counter[1].innerHTML);