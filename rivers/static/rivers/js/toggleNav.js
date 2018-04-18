var navOpen=false;
function toggleNav() {
    if (navOpen){
        document.getElementById("myNav").classList.remove('active');
        buttons = document.getElementsByClassName("closebtn")
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }
        navOpen=false
    } else {
        document.getElementById("myNav").classList.add('active');
        buttons = document.getElementsByClassName("closebtn")
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.add('active');
        }
        navOpen=true;
    }
}

function clickHandler(e){
    classes = e.target.classList;
    if (!classes.contains("closebtn")){
           if (navOpen){
            toggleNav();
        }
    }
}

var element = document.getElementById('wholepage');
element.addEventListener('click', clickHandler);