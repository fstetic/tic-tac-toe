import tkinter as tk
import tkinter.font as tkfont
import game

class Window(tk.Frame):

	def __init__(self, root=None):
		super().__init__(root)
		self.root = root
		self.winfo_toplevel().title("Tic-Tac-Toe")
		self.grid(sticky="nsew")
		for i in range(3):
			self.grid_columnconfigure(i,weight=1)
			self.grid_rowconfigure(i, weight=1)
		self.fields = [tk.Canvas(self, bg="white", bd=4) for i in range(9)]
		for i in range(9):
			self.fields[i].grid(row=int(i / 3), column=i % 3, sticky="nsew")
			self.fields[i].symbol = None
		self.update()
		self.choose_window = tk.Toplevel(self, bg="white")
		self.choose_window.title("Setup")
		self.choose_window.resizable(width=False, height=False)
		self.o_button, self.x_button = tk.Button(self.choose_window), tk.Button(self.choose_window)
		self.choose_symbol()

	def choose_symbol(self):
		self.choose_window.geometry("500x350+{}+{}".format(int(self.winfo_width()/3), int(self.winfo_height()/3)))
		self.choose_window.attributes('-topmost', 'true')
		self.choose_window.protocol('WM_DELETE_WINDOW', exit)
		self.choose_window.grid()
		self.choose_window.rowconfigure(0, minsize=80)
		self.choose_window.rowconfigure(2, minsize=80)
		tk.Label(self.choose_window, bg="white", fg="black", text="Choose which symbol you want to use: ",
		         font=tkfont.Font(family="likhan", size=25, weight='bold')).grid(row=0, column=0, columnspan=2)
		o_image, x_image = tk.PhotoImage(file = 'o.png'), tk.PhotoImage(file = 'x.png')
		self.o_button.config(image = o_image, command=lambda arg=self: arg.choose_order('o'))
		self.x_button.config(image = x_image, command=lambda arg=self: arg.choose_order('x'))
		self.o_button.grid(row=1, column=0)
		self.x_button.grid(row=1, column=1)
		self.o_button.image, self.x_button.image = o_image, x_image   # saving reference so the image doesn't get cleared by the garbage-collector
		
	def choose_order(self, symbol):
		tk.Label(self.choose_window, bg="white", fg="black", text="Do you want to go first?",
		         font=tkfont.Font(family="likhan", size=25, weight='bold')).grid(row=2, column=0, columnspan=2)
		tk.Button(self.choose_window, text="Yes", bg="white", fg="black", width=4, height=2,
		          command=lambda arg=self: game.play(arg, symbol, True)).grid(row=3,column=0)
		tk.Button(self.choose_window, text="No", bg="white", fg="black", width=4, height=2,
		          command=lambda arg=self: game.play(arg, symbol, False)).grid(row=3, column=1)
