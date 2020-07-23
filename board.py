import tkinter as tk

class Window(tk.Frame):
	def __init__(self, root=None):
		super().__init__(root)
		self.root = root
		self.grid(sticky="nsew")
		for i in range(3):
			self.grid_columnconfigure(i,weight=1)
			self.grid_rowconfigure(i, weight=1)
		self.fields = [tk.Canvas(self, bg="white", bd=4).grid(row=int(i/3), column=i%3, sticky="nsew") for i in range(9)]