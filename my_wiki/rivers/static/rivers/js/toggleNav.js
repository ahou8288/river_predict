var navOpen=false;
function toggleNav() {
    if (navOpen){
        document.getElementById("myNav").style.minWidth = "0%";
        document.getElementById("navbutton").classList.remove('active')
        document.getElementById("pagebutton").classList.remove('active')
        navOpen=false
    } else {
        document.getElementById("myNav").style.minWidth = "30em";
        document.getElementById("navbutton").classList.add('active')
        document.getElementById("pagebutton").classList.add('active')
        navOpen=true;
    }
}