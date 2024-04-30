gsap.from('.container', {opacity:0, duration: 1, delay: 0.5, y:1}); 
gsap.from('.move', {opacity:0, duration: 1, delay: 0.5, y:1}); 
gsap.from('.general', {opacity:0, duration: 1, delay: 0.5, y:1});

document.addEventListener('mousemove', move);
function move(e){
    this.querySelectorAll('.move').forEach(layer =>{
        const speed = layer.getAttribute('data-speed')

        const x = (window.innerWidth - e.pageX*speed)/120
        const y = (window.innerWidth - e.pageY*speed)/120

        layer.style.transform = `translateX(${x}px) translateY(${y}px)`
    })
}


const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});




