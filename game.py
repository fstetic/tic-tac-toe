import tkinter as tk
import tkinter.font as tkfont
import board
import minimax


def play(window, symbol, player_first):
	window.choose_window.destroy()
	if symbol=='o':
		for field in window.fields:
			field.bind('<ButtonPress>', lambda event, arg=window: draw(event, 'o', arg))
			field.bind('<ButtonRelease>', lambda event, arg=window: ai_move(event, 'x', 'o', arg))
		if not player_first:
			ai_move(tk.Event(), 'x', 'o', window, True)
	else:
		for field in window.fields:
			field.bind('<ButtonPress>', lambda event, arg=window: draw(event, 'x', arg))
			field.bind('<ButtonRelease>', lambda event, arg=window: ai_move(event, 'o', 'x', arg))
		if not player_first:
			ai_move(tk.Event(), 'o', 'x', window, True)


def draw(event, symbol, window):
	height, width = event.widget.winfo_height(), event.widget.winfo_width()
	center_x, center_y = int(width/2), int(height/2)
	r = min(width-center_x, height-center_y)
	if symbol=='o':
		event.widget.create_oval(center_x-r+10,center_y-r+10, center_x+r-10, center_y+r-10, width=4)    # O
		event.widget.symbol = 'o'
	else:
		event.widget.create_line(center_x-r+10,center_y-r+10, center_x+r-10, center_y+r-10, width=4)    # \
		event.widget.create_line(center_x-r+10, center_y+r-10, center_x+r-10, center_y-r+10, width=4)   # /
		event.widget.symbol = 'x'
	event.widget.unbind('<ButtonPress>')
	win_symbol, win_fields, command = check_if_end_move([field.symbol for field in window.fields])
	if command != "continue":
		for canvas in window.fields:
			canvas.unbind("<ButtonPress>")
			canvas.unbind("<ButtonRelease>")
		end_game(window, win_fields, win_symbol, width, height, center_x, center_y, command)


# takes a list which represents the board where 'x' is X, 'o' is O, and None is empty field
# returns symbol which won, winning fields and string saying orientation of winning fields
def check_if_end_move(layout):
	# rows
	for i in range(0,7,3):
		win_symbol = {layout[i], layout[i+1], layout[i+2]}
		if len(win_symbol) == 1 and None not in win_symbol:
			return win_symbol.pop(), [i, i+1, i+2], "row"
	# columns
	for i in range(0,3):
		win_symbol = {layout[i], layout[i+3], layout[i+6]}
		if len(win_symbol) == 1 and None not in win_symbol:
			return win_symbol.pop(), [i, i+3, i+6], "column"
	# diagonals
	win_symbol = {layout[0], layout[4], layout[8]}
	if len(win_symbol) == 1 and None not in win_symbol:
		return win_symbol.pop(), [0,4,8], "diag left"
	win_symbol = {layout[2], layout[4], layout[6]}
	if len(win_symbol) == 1 and None not in win_symbol:
		return win_symbol.pop(), [2,4,6], "diag right"
	# tie
	if None not in [layout[i] for i in range(9)]:
		return None, [], "tie"
	# not end
	return None, [], "continue"


# draws a line across winning fields
def end_game(window, win_fields, symbol, x, y, center_x, center_y, command):
	label_text = tk.StringVar()
	if command == "tie":
		label_text.set("It's a tie!")
	else:
		label_text.set("{} wins!".format(symbol.upper()))
		if command == "row":
			for field in win_fields:
				window.fields[field].create_line(0, center_y, x, center_y, width=4)
		elif command == "column":
			for field in win_fields:
				window.fields[field].create_line(center_x, 0, center_x, y, width=4)
		elif command == "diag left":
			for field in win_fields:
				window.fields[field].create_line(0, 0, x, y, width=4)
		elif command == "diag right":
			for field in win_fields:
				window.fields[field].create_line(0, y, x, 0, width=4)
	call_end_window(window, label_text)


def call_end_window(window, text):
	win_window = tk.Toplevel(window, bg="white")
	win_window.title("Game end")
	win_window.geometry("300x100+{}+{}".format(int(window.winfo_rootx()+300), int(window.winfo_rooty()+100)))   # center the window considering TopLevel
	win_window.attributes('-topmost', 'true')
	win_window.resizable(width=False, height=False)
	win_window.grid()
	for i in range(2):
		win_window.grid_rowconfigure(i, weight=1)
		win_window.grid_columnconfigure(i, weight=1)
	tk.Label(win_window, bg="white", fg="black", textvariable=text,
	         font=tkfont.Font(family="likhan", size=25, weight='bold')).grid(row=0, column=0, columnspan=2)
	tk.Button(win_window, text="Play again", bg="white", fg="black", command=lambda arg=window:play_again(arg)).grid(row=1,column=0)
	tk.Button(win_window, text="Exit", bg="white", fg="black", command=exit).grid(row=1,column=1)
	win_window.protocol('WM_DELETE_WINDOW', exit)


def play_again(window):
	window.root.destroy()
	main()


def ai_move(event, ai_symbol, player_symbol, window, ai_first=False):
	if not ai_first:
		event.widget.unbind('<ButtonRelease>')
	current_layout = [field.symbol for field in window.fields]
	if None not in current_layout:      # if the player did the last move
		return
	index = minimax.get_next_move(current_layout, ai_symbol, player_symbol)
	fake_event = tk.Event()
	fake_event.widget = window.fields[index]
	window.fields[index].unbind('<ButtonRelease>')
	draw(fake_event, ai_symbol, window)


def main():
	root = tk.Tk()
	root.geometry("900x700+{}+{}".format(int(root.winfo_screenwidth()/2-450), int(root.winfo_screenheight()/2-350)))    # center window on screen
	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)
	icon = tk.PhotoImage(file = "icon.png")
	root.iconphoto(True, icon)
	window = board.Window(root)
	window.mainloop()


if __name__ == '__main__':
	main()
