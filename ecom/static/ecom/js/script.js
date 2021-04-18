function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
    document.querySelector('body').style.overflow = 'hidden'
  }
  
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.querySelector('body').style.overflow = 'auto'
}


// ON SCROLL TRIGGER NAV COLOR

const navbar = document.querySelector('.navbar');
window.onscroll = () => {
    if (window.scrollY > 100) {
        navbar.classList.add('nav-active');
    } else {
        navbar.classList.remove('nav-active');
    }
};