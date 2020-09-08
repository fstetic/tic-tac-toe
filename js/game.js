let playerSymbol, computerSymbol;

function addListeners(){
	for (let i = 0; i < 9; i++) {
		document.getElementById(i.toString()).addEventListener("click", displaySymbol)
	}
	document.getElementById("x_button").addEventListener("click", start)
	document.getElementById("o_button").addEventListener("click", start)
}

function start(event) {
	playerSymbol = event.target.textContent === 'X' ? 'X' : 'O';
	computerSymbol = event.target.textContent === 'X' ? 'O' : 'X';
	document.getElementById("x_button").hidden = true
	document.getElementById("o_button").hidden = true
}

function displaySymbol(event) {
	let button = event.target
	button.textContent = playerSymbol
}
