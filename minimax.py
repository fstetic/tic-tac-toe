import game
import math

def get_next_move(state, symbol):
	moves = get_next_states(state, symbol)
	outcomes = [max_value(s, symbol) for s in moves]
	next_move = moves[outcomes.index(min(outcomes))]
	for i in range(9):
		if next_move[i] != state[i]:
			return i

def max_value(state, symbol, alpha=-math.inf, beta=math.inf):
	if None not in state:
		return last_move(state, symbol)
	outcome = alpha
	for s in get_next_states(state, symbol):
		outcome = max(outcome, min_value(s, symbol, alpha, beta))
		if outcome >= beta:     # beta pruning
			return beta
	return outcome

def min_value(state, symbol, alpha, beta):
	if None not in state:
		return last_move(state, symbol)
	outcome = beta
	for s in get_next_states(state, symbol):
		outcome = min(outcome, max_value(s, symbol, alpha, beta))
		if outcome <= alpha:    # alpha pruning
			return alpha
	return outcome

def last_move(all_symbols, symbol):
	win_symbol, win_fields, command = game.check_end_move(all_symbols)
	if win_symbol == symbol:
		return 1
	elif win_symbol is None:
		return 0
	else:
		return -1

def get_next_states(state, symbol):
	result = list()
	for i in range(9):
		if state[i] is None:
			next_state = state.copy()
			next_state[i] = symbol
			result.append(next_state)
	return result