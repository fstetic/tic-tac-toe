import game
import math

def get_next_move(state, ai_symbol, player_symbol):
	moves = get_next_states(state, ai_symbol)
	outcomes = [min_value(s, ai_symbol, player_symbol, 0) for s in moves]
	next_move = moves[outcomes.index(max(outcomes))]
	for i in range(9):
		if next_move[i] != state[i]:
			return i

def max_value(state, ai_symbol, player_symbol, depth, alpha=-math.inf, beta=math.inf):
	terminal = last_move(state, ai_symbol, depth)
	if terminal != 2:
		return terminal
	outcome = alpha
	all_next = get_next_states(state, ai_symbol)
	for s in all_next:
		outcome = max(outcome, min_value(s, ai_symbol, player_symbol, depth+1, outcome, beta))
		if outcome >= beta:     # beta pruning
			return beta
	return outcome

def min_value(state, ai_symbol, player_symbol, depth, alpha=-math.inf, beta=math.inf):
	terminal = last_move(state, ai_symbol, depth)
	if terminal != 2:
		return terminal
	outcome = beta
	all_next = get_next_states(state, player_symbol)
	for s in all_next:
		outcome = min(outcome, max_value(s, ai_symbol, player_symbol, depth+1, alpha, outcome))
		if outcome <= alpha:    # alpha pruning
			return alpha
	return outcome

def last_move(all_symbols, symbol, depth):
	win_symbol, win_fields, command = game.check_end_move(all_symbols)
	if command != "continue":
		if win_symbol == symbol:
			return 10-depth
		elif win_symbol is None:
			return 0
		else:
			return -10+depth
	return 2


def get_next_states(state, symbol):
	if None not in state:
		return [state]
	result = list()
	for i in range(9):
		if state[i] is None:
			temp_state = state.copy()
			temp_state[i] = symbol
			result.append(temp_state)
	return result