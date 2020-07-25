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
		self.choose_window.title("Choose symbol")
		self.choose_window.resizable(width=False, height=False)
		self.o_button, self.x_button = tk.Button(self.choose_window), tk.Button(self.choose_window)
		self.choose_symbol()

	def choose_symbol(self):
		self.choose_window.geometry("500x250+{}+{}".format(int(self.winfo_width()/3), int(self.winfo_height()/3)))
		self.choose_window.attributes('-topmost', 'true')
		self.choose_window.grid()
		tk.Label(self.choose_window, bg="white", fg="LightSteelBlue4", text="Choose which symbol you want to use: ",
		         font=tkfont.Font(family="likhan", size=25, weight='bold')).grid(row=0, column=0, columnspan=2)
		o_image, x_image = tk.PhotoImage(file = 'o.png'), tk.PhotoImage(file = 'x.png')
		self.o_button.config(image = o_image, command=lambda arg=self: game.play(arg, 'o'))
		self.x_button.config(image = x_image, command=lambda arg=self: game.play(arg, 'x'))
		self.o_button.grid(row=1, column=0)
		self.x_button.grid(row=1, column=1)
		self.o_button.image, self.x_button.image = o_image, x_image   # saving reference so the image doesn't get cleared by the garbage-collector

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry("900x600")
	root.grid_rowconfigure(0, weight=1)
	root.grid_columnconfigure(0, weight=1)
	window = Window(root)
	window.mainloop()