let playerSymbol, computerSymbol;
let field = []

function addListeners(){
	document.getElementById("x_button").addEventListener("click", start)
	document.getElementById("o_button").addEventListener("click", start)
	document.getElementById("play_again").addEventListener("click", restart)
}

function start(event) {
	for (let i = 0; i < 9; i++) {
		document.getElementById(i.toString()).addEventListener("click", playerMove)
		field.push('-')
	}
	document.getElementById("x_button").hidden = true
	document.getElementById("o_button").hidden = true
	if (event.target.textContent === 'X'){
		playerSymbol = 'X'
		computerSymbol = 'O'
	} else {
		playerSymbol = 'O'
		computerSymbol = 'X'
		computerMove()
	}
}

function displaySymbol(button, symbol) {
	button.textContent = symbol
	field[button.id] = symbol
	button.removeEventListener("click", playerMove)
	let winningFields = checkIfEndMove()
	if(winningFields.length !== 0){
		endGame(winningFields)
	}
}

function playerMove(event){
	displaySymbol(event.target, playerSymbol)
	computerMove()
}

function computerMove(){
	if(!field.includes('-')) return
	let rand;
	do{
		rand = Math.floor(Math.random() * 9)
	} while(field[rand] !== '-')
	let button = document.getElementById(rand.toString())
	displaySymbol(button, computerSymbol)
}

function checkIfEndMove(){
	let winningFields = new Set()
	// rows
	for(let i=0;i<7;i+=3){
		[field[i], field[i+1], field[i+2]].forEach(item => winningFields.add(item))
		if(winningFields.size === 1 && !winningFields.has('-')) {
			return [i, i+1, i+2]
		}
		winningFields.clear()
	}
	// columns
	for(let i=0;i<3;i++){
		[field[i], field[i+3], field[i+6]].forEach(item => winningFields.add(item))
		if(winningFields.size === 1 && !winningFields.has('-')) {
			return [i, i+3, i+6]
		}
		winningFields.clear()
	}

	// diagonals
	winningFields.add(field[0]);
	winningFields.add(field[4]);
	winningFields.add(field[8]);
	if(winningFields.size === 1 && !winningFields.has('-')) {
		return [0,4,8]
	}
	winningFields.clear()

	winningFields.add(field[2]);
	winningFields.add(field[4]);
	winningFields.add(field[6]);
	if(winningFields.size === 1 && !winningFields.has('-')) {
		return [2,4,6]
	}

	if(!field.includes('-')) return [1]	// tie
	return []
}

function endGame(winningFields){
	for (let i = 0; i < 9; i++) {
		document.getElementById(i.toString()).removeEventListener("click", playerMove)
	}
	if(winningFields.length === 1){
		document.getElementById('end_game_text').textContent = "It's a tie!"
	} else {
		winningFields.forEach(item => document.getElementById(item.toString()).style.color = '#FF9900')
		if(field[winningFields[0]] === playerSymbol){
			document.getElementById('end_game_text').textContent = "You win!"
		} else {
			document.getElementById('end_game_text').textContent = "You lose!"
		}
	}
	document.getElementById('play_again').style.display = 'block'
}

function restart(){
	document.getElementById("x_button").hidden = false
	document.getElementById("o_button").hidden = false
	document.getElementById('end_game_text').textContent = ''
	document.getElementById('play_again').style.display = 'none'
	field = []
	for (let i = 0; i < 9; i++) {
		document.getElementById(i.toString()).textContent = ''
		document.getElementById(i.toString()).style.color = 'black'
	}
}