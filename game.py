import tkinter as tk
import tkinter.font as tkfont

def play(window, symbol):
	window.choose_window.destroy()
	if symbol=='o':
		for i in range(9):
			window.fields[i].bind('<ButtonPress>', lambda event=i, arg=window: draw(event, 'o', arg))
	else:
		for i in range(9):
			window.fields[i].bind('<ButtonPress>', lambda event=i, arg=window: draw(event, 'x', arg))


def draw(event, symbol, window):
	height, width = event.widget.winfo_height(), event.widget.winfo_width()
	center_x, center_y = int(width/2), int(height/2)
	r = min(width-center_x, height-center_y)
	if symbol=='o':
		event.widget.create_oval(center_x-r+10,center_y-r+10, center_x+r-10, center_y+r-10, width=4)
		event.widget.symbol = 'o'
	else:
		event.widget.create_line(center_x-r+10,center_y-r+10, center_x+r-10, center_y+r-10, width=4)    # \
		event.widget.create_line(center_x-r+10, center_y+r-10, center_x+r-10, center_y-r+10, width=4)   # /
		event.widget.symbol = 'x'
	event.widget.unbind('<ButtonPress>')
	win_symbol, win_fields, command = check_end_move(window)
	end(window, win_fields, win_symbol, width, height, center_x, center_y, command)


def check_end_move(window):
	# rows
	for i in range(0,7,3):
		symbol = {window.fields[i].symbol, window.fields[i+1].symbol, window.fields[i+2].symbol}
		if len(symbol) == 1 and None not in symbol:
			return window.fields[i].symbol, [i, i+1, i+2], "row"
	# columns
	for i in range(0,3):
		symbol = {window.fields[i].symbol, window.fields[i + 3].symbol, window.fields[i + 6].symbol}
		if len(symbol) == 1 and None not in symbol:
			return window.fields[i].symbol, [i, i+3, i+6], "column"
	# diagonals
	symbol = {window.fields[0].symbol, window.fields[4].symbol, window.fields[8].symbol}
	if len(symbol) == 1 and None not in symbol:
		return window.fields[0].symbol, [0,4,8], "diag left"
	symbol = {window.fields[2].symbol, window.fields[4].symbol, window.fields[6].symbol}
	if len(symbol) == 1 and None not in symbol:
		return window.fields[2].symbol, [2,4,6], "diag right"
	# tie
	if None not in [window.fields[i].symbol for i in range(9)]:
		return None, [], "tie"
	return None, [], "continue"


def end(window, win_fields, symbol, x, y, center_x, center_y, command):
	label_text = tk.StringVar()
	if command == "continue":
		return
	elif command == "tie":
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
	win_window.geometry("300x100+{}+{}".format(int(window.winfo_width() / 3), int(window.winfo_height() / 3)))
	win_window.attributes('-topmost', 'true')
	win_window.resizable(width=False, height=False)
	win_window.grid()
	for i in range(2):
		win_window.grid_rowconfigure(i, weight=1)
		win_window.grid_columnconfigure(i, weight=1)
	tk.Label(win_window, bg="white", fg="LightSteelBlue4", textvariable=text,
	         font=tkfont.Font(family="likhan", size=25, weight='bold')).grid(row=0, column=0, columnspan=2)
	tk.Button(win_window, text="Play again", bg="white", fg="black").grid(row=1,column=0)
	tk.Button(win_window, text="Exit", bg="white", fg="black", command=exit).grid(row=1,column=1)
