
def play(window, symbol):
	window.choose_window.destroy()
	if symbol=='o':
		for i in range(9):
			window.fields[i].bind('<ButtonPress>', lambda event=i: draw(event, 'o'))
	else:
		for i in range(9):
			window.fields[i].bind('<ButtonPress>', lambda event=i: draw(event, 'x'))


def draw(event, symbol):
	height, width = event.widget.winfo_height(), event.widget.winfo_width()
	center_x, center_y = int(width/2), int(height/2)
	r = min(width-center_x, height-center_y)
	if symbol=='o':
		event.widget.create_oval(center_x-r+10,center_y-r+10, center_x+r-10, center_y+r-10, width=4)
	else:
		event.widget.create_line(center_x-r+10,center_y-r+10, center_x+r-10, center_y+r-10, width=4)    # \
		event.widget.create_line(center_x-r+10, center_y+r-10, center_x+r-10, center_y-r+10, width=4)   # /
	event.widget.unbind('<ButtonPress>')
