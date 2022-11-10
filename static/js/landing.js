var navbtn = document.getElementById('nav-btn')
var navMenu = document.getElementById('nav-menu')
var close = document.getElementById('close-nav')


navbtn.addEventListener("click", ()=>{
	navMenu.classList.add('show-nav');
})

close.addEventListener("click", ()=>{
	navMenu.classList.remove('show-nav')
})