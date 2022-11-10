const log = document.getElementById('login-title');
var selector = document.getElementById('select');
const reg = document.getElementById('reg-title');
const form = document.getElementById('form');
const logForm = document.getElementById('login-form');
const regForm = document.getElementById('reg-form');
console.log(form)

log.addEventListener("click", ()=>{

	selector.classList.add('move-selector');
	form.classList.add('log-form-display');
	logForm.classList.add('opacity');
	regForm.classList.add('rem-opac');
})

reg.addEventListener("click", ()=>{

	selector.classList.remove('move-selector')
	form.classList.remove('log-form-display')
	logForm.classList.remove('opacity');
	regForm.classList.remove('rem-opac');

})
