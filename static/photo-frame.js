
function next(){
	fetch("/next",{method:"POST"})
}
function remove(){
	fetch("/noshow",{method:"POST"})
}
function crop(){
	fetch("/markforcrop", {method:"POST"})
}

function favourite(){
	fetch("/markfavourite", {method:"POST"})
}

function rescan(){
	fetch("/scan", {method:"POST"})
}

