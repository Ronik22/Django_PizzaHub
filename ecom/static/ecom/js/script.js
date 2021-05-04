// FLASH MESSAGES
var close = document.getElementsByClassName("closebtnmsg");
var i;

for (i = 0; i < close.length; i++) {
  close[i].onclick = function(){
    var div = this.parentElement;
    div.style.opacity = "0";
    setTimeout(function(){ div.style.display = "none"; }, 600);
  }
}

function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
    document.querySelector('body').style.overflow = 'hidden'
  }
  
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.querySelector('body').style.overflow = 'auto'
}


function openSearch() {
    document.getElementById("myOverlay").style.display = "block";
    document.querySelector('body').style.overflow = 'hidden'
}
function closeSearch() {
    document.getElementById("myOverlay").style.display = "none";
    document.querySelector('body').style.overflow = 'auto'
}

// ON SCROLL TRIGGER NAV COLOR

const navbar = document.querySelector('.mynavbar');
window.onscroll = () => {
    if (window.scrollY > 100) {
        navbar.classList.add('nav-active');
    } else {
        navbar.classList.remove('nav-active');
    }
};
