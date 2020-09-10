let playerSymbol, computerSymbol;
let board = []

function addListeners(){
	document.getElementById("x_button").addEventListener("click", start)
	document.getElementById("o_button").addEventListener("click", start)
	document.getElementById("play_again").addEventListener("click", restart)
}

function start(event) {
	for (let i = 0; i < 9; i++) {
		document.getElementById(i.toString()).addEventListener("click", playerMove)
		board.push('-')
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
	board[button.id] = symbol
	button.removeEventListener("click", playerMove)
	let winningFields = checkIfEndMove(board)
	if(winningFields.length !== 0){
		endGame(winningFields)
	}
}

function playerMove(event){
	displaySymbol(event.target, playerSymbol)
	computerMove()
}

function computerMove(){
	if(!board.includes('-')) return
	let button = document.getElementById(nextMove())
	displaySymbol(button, computerSymbol)
}

function checkIfEndMove(board){
	let winningFields = new Set()
	// rows
	for(let i=0;i<7;i+=3){
		[board[i], board[i+1], board[i+2]].forEach(item => winningFields.add(item))
		if(winningFields.size === 1 && !winningFields.has('-')) {
			return [i, i+1, i+2]
		}
		winningFields.clear()
	}
	// columns
	for(let i=0;i<3;i++){
		[board[i], board[i+3], board[i+6]].forEach(item => winningFields.add(item))
		if(winningFields.size === 1 && !winningFields.has('-')) {
			return [i, i+3, i+6]
		}
		winningFields.clear()
	}

	// diagonals
	winningFields.add(board[0]);
	winningFields.add(board[4]);
	winningFields.add(board[8]);
	if(winningFields.size === 1 && !winningFields.has('-')) {
		return [0,4,8]
	}
	winningFields.clear()

	winningFields.add(board[2]);
	winningFields.add(board[4]);
	winningFields.add(board[6]);
	if(winningFields.size === 1 && !winningFields.has('-')) {
		return [2,4,6]
	}

	if(!board.includes('-')) return [1]	// tie
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
		if(board[winningFields[0]] === playerSymbol){
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
	board = []
	for (let i = 0; i < 9; i++) {
		document.getElementById(i.toString()).textContent = ''
		document.getElementById(i.toString()).style.color = 'black'
	}
}

// minimax part
function nextMove(){
	let moves = getAllMoves(board, computerSymbol)		// list of all possible states
	let outcomes = []		// list of outcomes for those states
	for(let i=0; i<moves.length;i++) {
		outcomes.push(minValue(moves[i], 0))
	}
	let moveToDo = moves[outcomes.indexOf(Math.max(...outcomes))]		// next move is the highest rated one
	for(let i=0;i<9;i++){
		if(moveToDo[i] !== board[i]) return i
	}
}

function maxValue(boardState, depth, alpha, beta){
	let terminal = checkIfLastMove(boardState, depth)
	if(terminal !== 'none') return terminal
	let outcome = alpha
	let allMoves = getAllMoves(boardState, computerSymbol)
	for(let i=0;i<allMoves.length;i++){
		outcome = Math.max(outcome, minValue(allMoves[i], depth+1, outcome, beta))
		if(outcome >= beta) return beta
	}
	return outcome
}

function minValue(boardState, depth, alpha= - Infinity, beta = Infinity){
	let terminal = checkIfLastMove(boardState, depth)
	if(terminal !== 'none') return terminal
	let outcome = beta
	let allMoves = getAllMoves(boardState, playerSymbol)
	for(let i=0;i<allMoves.length;i++){
		outcome = Math.min(outcome, maxValue(allMoves[i], depth+1, alpha, outcome))
		if(outcome <= alpha) return alpha
	}
	return outcome
}

function checkIfLastMove(boardState, depth){
	let winningFields = checkIfEndMove(boardState)
	if(winningFields.length !== 0){
		if(winningFields.length === 1) return 0		// tie
		let winSymbol = boardState[winningFields[0]]	// find out who won
		if (winSymbol === computerSymbol) return 10 - depth
		else return -10 + depth
	}
	return 'none'
}

function getAllMoves(boardState, symbol){
	if(!boardState.includes('-')) return [boardState]
	let result = []
	for(let i=0;i<9;i++){
		if (boardState[i] === '-') {
			let temp = [...boardState]
			temp[i] = symbol
			result.push(temp)
		}
	}
	return result
}