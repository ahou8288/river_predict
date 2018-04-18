desc=document.getElementById('id_description');

function auto_grow() {
    desc.style.height = "5px";
    desc.style.height = (desc.scrollHeight)+"px";
}

desc.addEventListener('keyup',auto_grow);

auto_grow();