var cancel = document.getElementById('can')
var main = document.getElementById('main')
var box = document.getElementById('can-box')
var close = document.getElementById('can-close')

var search = document.getElementById('search')
var sClose = document.getElementById('search-close')
var sButton = document.getElementById('sButton')

var result = document.getElementById('res')
var resBox = document.getElementById('result-box')

var select = document.getElementById('select')
var todayTitle = document.getElementById('today-title')
var overTitle = document.getElementById('overall-title')
var today = document.getElementById('today')
var overall = document.getElementById('overall')

todayTitle.addEventListener("click", ()=>{
	select.classList.add('tab-select')
	/*today.classList.add('tab-show')*/
	overall.classList.add('tab-hide')
})

overTitle.addEventListener("click", ()=>{
	select.classList.remove('tab-select')
	/*today.classList.remove('show')*/
	overall.classList.remove('tab-hide')
})

cancel.addEventListener("click", ()=>{
	box.classList.add('show')
	main.classList.add('blur')
})

close.addEventListener("click", ()=>{
	box.classList.remove('show')
	main.classList.remove('blur')
})

sButton.addEventListener("click", ()=>{
	search.classList.add('show')
	main.classList.add('blur')
})

sClose.addEventListener("click", ()=>{
	search.classList.remove('show')
	main.classList.remove('blur')
})


result.addEventListener("click", ()=>{
	resBox.classList.add('hide')
})