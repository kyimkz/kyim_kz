let navbar = document.querySelector('.header .navbar')

document.querySelector('#menu').onclick = () =>{
  navbar.classList.add('active');
}

document.querySelector('#close').onclick = () =>{
  navbar.classList.remove('active');
}


// mousemove home img

document.addEventListener('mousemove', move);
function move(e){
  this.querySelectorAll('.move').forEach(layer =>{
    const speed = layer.getAttribute('data-speed')

    const x = (window.innerWidth - e.pageX*speed)/120
    const y = (window.innerWidth - e.pageY*speed)/120

    layer.style.transform = `translateX(${x}px) translateY(${y}px)`

  })
}



gsap.from('.logo', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.navbar .nav_item', {opacity: 0, duration: 1, delay: 1.1, y:30});
gsap.from('.image_login', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.function', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.new_season', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.links', {opacity: 0, duration: 1, delay: 1.8, y:10});
gsap.from('.btn', {opacity: 0, duration: 1, delay: 1.8, y:10});
gsap.from('.navbabba', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('#gen', {opacity:0, duration: 1, delay: 0.5, y:10});
gsap.from('.gen_for_price', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.afkfc', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.delete-wishlist-product', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.add-to-cart-btn', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.djskadjc', {opacity: 0, duration: 1, delay: 1, y:10});

gsap.from('.h1', {opacity: 0, duration: 1, delay: 1.9, y:30, stagger: 0.7});
gsap.from('.h2', {opacity: 0, duration: 1, delay: 1.9, y:30, stagger: 0.7});
gsap.from('.gen', {opacity: 0, duration: 1, delay: 1.9, y:30, stagger: 0.7});
gsap.from('.body', {opacity: 0, duration: 1, delay: 1.9, y:30, stagger: 0.7});

gsap.from('.title', {opacity: 0, duration: 1, delay: 0.6, y:30});
gsap.from('.description', {opacity: 0, duration: 1, delay: 0.8, y:30});
gsap.from('.image', {opacity: 0, duration: 1, delay: 1.6, y:30});


gsap.from('.footer', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.pages', {opacity: 0, duration: 1, delay: 1, y:10});
gsap.from('.general', {opacity: 0, duration: 1, delay: 1, y:10});


jQuery(window).on('scroll', function() {
  if(jQuery(window).scrollTop() > 50) {
      jQuery('#header_frame').css('background-color', 'var(--color-bg)');
  } else {
     jQuery('#header_frame').css('background-color', 'transparent');
  }
});


$(window).on("load",function(){
  $(".loader-wrapper").fadeOut("slow");
});




var imgs = document.querySelectorAll('.slider img');
var dots = document.querySelectorAll('.dot');
var currentImg = 0; // index of the first image 
const interval = 3000; // duration(speed) of the slide


function changeSlide(n) {
    for (var i = 0; i < imgs.length; i++) { // reset
      imgs[i].style.opacity = 0;
      dots[i].className = dots[i].className.replace(' active', '');
    }
  
    currentImg = n;
  
    imgs[currentImg].style.opacity = 1;
    dots[currentImg].className += ' active';
  }



function myFunction() {
  var x = document.getElementById("myLinks");
  if (x.style.display === "none") {
    x.style.display = "block";
    x.style.transition = ".9s ease-in-out";
  } else {
    x.style.display = "none";
    x.style.transition = ".9s ease-in-out";
  }
}





const theme = localStorage.getItem('theme');


/**
* Utility function to calculate the current theme setting.
* Look for a local storage value.
* Fall back to system setting.
* Fall back to light mode.
*/
function calculateSettingAsThemeString({ localStorageTheme, systemSettingDark }) {
  if (localStorageTheme !== null) {
    return localStorageTheme;
  }

  if (systemSettingDark.matches) {
    return "dark";
  }

  return "light";
}

/**
* Utility function to update the button text and aria-label.
*/
function updateButton({ buttonEl, isDark }) {
  const newCta = isDark ? 'light' : 'dark';
  // use an aria-label if you are omitting text on the button
  // and using a sun/moon icon, for example
  buttonEl.setAttribute("aria-label", newCta);
  buttonEl.innerText = newCta;
}
/**
* Utility function to update the theme setting on the html tag
*/
function updateThemeOnHtmlEl({ theme }) {
  document.querySelector("html").setAttribute("data-theme", theme);
}


/**
* On page load:
*/

/**
* 1. Grab what we need from the DOM and system settings on page load
*/
const button = document.querySelector("[data-theme-toggle]");
const localStorageTheme = localStorage.getItem("theme");
const systemSettingDark = window.matchMedia("(prefers-color-scheme: dark)");

/**
* 2. Work out the current site settings
*/
let currentThemeSetting = calculateSettingAsThemeString({ localStorageTheme, systemSettingDark });

/**
* 3. Update the theme setting and button text accoridng to current settings
*/
updateButton({ buttonEl: button, isDark: currentThemeSetting === "dark" });
updateThemeOnHtmlEl({ theme: currentThemeSetting });

/**
* 4. Add an event listener to toggle the theme
*/
button.addEventListener("click", (event) => {
  const newTheme = currentThemeSetting === "dark" ? "light" : "dark";

  localStorage.setItem("theme", newTheme);
  updateButton({ buttonEl: button, isDark: newTheme === "dark" });
  updateThemeOnHtmlEl({ theme: newTheme });

  currentThemeSetting = newTheme;
}); 