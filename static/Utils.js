const badge_theme = {
    blueL : "block px-3 py-1 rounded-full text-sm font-medium bg-blue-50 text-blue-700 border border-blue-200",
    redL : "block px-3 py-1 rounded-full text-sm font-medium bg-red-50 text-red-700 border border-red-200",
}
const componet_badge = (value, theme) =>{
    let badge = document.createElement('span');
    badge.textContent = value || "Hey no insertaste un valor";
    badge.className = badge_theme[theme] || badge_theme["blueL"];
    return badge;
}

function replace_badge(value,theme, id){
    const Grupos = document.getElementById('Modules')
    const exist = Grupos.dataset.modulesExist === "true";
    const div = document.getElementById(id)
    div.innerHTML = ''
    if (exist){
     return div.appendChild(componet_badge(value,theme))
    }else{
        return div.appendChild(componet_badge("Oops!!! No tienes modulos xd","redL"))
    }
}


const marcaGrupo = (elemento, contenedorId)=>{
    const div = document.getElementById(contenedorId)
    div.querySelectorAll('.badge').forEach(el => {
        el.classList.remove('badge_select');
        el.textContent = el.textContent.replace("  ","").trim()
    });

    elemento.classList.add('badge_select');
    elemento.textContent = "  " + elemento.textContent.trim()
}
