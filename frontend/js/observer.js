
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
        } else {
            entry.target.classList.remove("visible");
        }
    });
}, {
    rootMargin: "0px 0px -15% 0px",
    threshold: 0.1
});

document.querySelectorAll(".mainLogo").forEach(element => observer.observe(element));