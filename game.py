import tkinter as tk
import tkinter.font as tkfont
import board
import minimax

def play(window, symbol, first):
	window.choose_window.destroy()
	if symbol=='o':
		for i in range(9):
			window.fields[i].bind('<ButtonPress>', lambda event, arg=window: draw(event, 'o', arg))
			window.fields[i].bind('<ButtonRelease>', lambda event, arg=window: opponent_move(event, 'x', arg))
		if not first:
			window.fields[0].event_generate('<ButtonRelease>')
			window.fields[0].bind('<ButtonRelease>', lambda event, arg=window: opponent_move(event, 'x', arg))
	else:
		for i in range(9):
			window.fields[i].bind('<ButtonPress>', lambda event, arg=window: draw(event, 'x', arg))
			window.fields[i].bind('<ButtonRelease>', lambda event, arg=window: opponent_move(event, 'o', arg))
		if not first:
			window.fields[0].event_generate('<ButtonRelease>')
			window.fields[0].bind('<ButtonRelease>', lambda event, arg=window: opponent_move(event, 'o', arg))



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
	win_symbol, win_fields, command = check_end_move([window.fields[i].symbol for i in range(9)])
	if command != "continue":
		for canvas in window.fields:
			canvas.unbind("<ButtonPress>")
			canvas.unbind("<ButtonRelease>")
		end(window, win_fields, win_symbol, width, height, center_x, center_y, command)


def check_end_move(symbols):
	# rows
	for i in range(0,7,3):
		win_symbol = {symbols[i], symbols[i+1], symbols[i+2]}
		if len(win_symbol) == 1 and None not in win_symbol:
			return win_symbol.pop(), [i, i+1, i+2], "row"
	# columns
	for i in range(0,3):
		win_symbol = {symbols[i], symbols[i+3], symbols[i+6]}
		if len(win_symbol) == 1 and None not in win_symbol:
			return win_symbol.pop(), [i, i+3, i+6], "column"
	# diagonals
	win_symbol = {symbols[0], symbols[4], symbols[8]}
	if len(win_symbol) == 1 and None not in win_symbol:
		return win_symbol.pop(), [0,4,8], "diag left"
	win_symbol = {symbols[2], symbols[4], symbols[6]}
	if len(win_symbol) == 1 and None not in win_symbol:
		return win_symbol.pop(), [2,4,6], "diag right"
	# tie
	if None not in [symbols[i] for i in range(9)]:
		return None, [], "tie"
	return None, [], "continue"


def end(window, win_fields, symbol, x, y, center_x, center_y, command):
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
	win_window.geometry("300x100+{}+{}".format(int(window.winfo_rootx()+300), int(window.winfo_rooty()+100)))
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


def opponent_move(event, symbol, window):
	event.widget.unbind('<ButtonRelease>')
	current_layout = [window.fields[i].symbol for i in range(9)]
	if None not in current_layout:
		return
	index = minimax.get_next_move(current_layout, symbol)
	fake_event = tk.Event()
	fake_event.widget = window.fields[index]
	window.fields[index].unbind('<ButtonRelease>')
	draw(fake_event, symbol, window)


def main():
	root = tk.Tk()
	root.geometry("900x700+{}+{}".format(int(root.winfo_screenwidth()/2-450), int(root.winfo_screenheight()/2-350)))
	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)
	icon = tk.PhotoImage(file = "icon.png")
	root.iconphoto(True, icon)
	window = board.Window(root)
	window.mainloop()


if __name__ == '__main__':
	main()
