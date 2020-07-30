import game
import math


def get_next_move(state_of_board, ai_symbol, player_symbol):
	moves = get_next_states(state_of_board, ai_symbol)
	outcomes = [min_value(s, ai_symbol, player_symbol, 0) for s in moves]
	next_move = moves[outcomes.index(max(outcomes))]
	for i in range(9):
		if next_move[i] != state_of_board[i]:
			return i


def max_value(state, ai_symbol, player_symbol, depth, alpha, beta):
	terminal = check_if_last_move(state, ai_symbol, depth)
	if terminal is not None:
		return terminal
	outcome = alpha
	for s in get_next_states(state, ai_symbol):
		outcome = max(outcome, min_value(s, ai_symbol, player_symbol, depth+1, outcome, beta))
		if outcome >= beta:     # beta pruning
			return beta
	return outcome


def min_value(state, ai_symbol, player_symbol, depth, alpha=-math.inf, beta=math.inf):
	terminal = check_if_last_move(state, ai_symbol, depth)
	if terminal is not None:
		return terminal
	outcome = beta
	for s in get_next_states(state, player_symbol):
		outcome = min(outcome, max_value(s, ai_symbol, player_symbol, depth+1, alpha, outcome))
		if outcome <= alpha:    # alpha pruning
			return alpha
	return outcome


# depth is used to encourage faster end
def check_if_last_move(layout, ai_symbol, depth):
	win_symbol, win_fields, command = game.check_if_end_move(layout)
	if command != "continue":   # if the game is over
		if win_symbol == ai_symbol:
			return 10 - depth
		elif win_symbol is None:
			return 0
		else:
			return -10 + depth
	return None


# returns list with all possible moves of given symbol
def get_next_states(state, symbol):
	if None not in state:
		return [state]
	result = list()
	for i, s in enumerate(state):
		if s is None:
			temp_state = state.copy()
			temp_state[i] = symbol
			result.append(temp_state)
	return result