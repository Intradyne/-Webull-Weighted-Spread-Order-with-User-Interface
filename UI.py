import tkinter as tk
from tkinter import messagebox as msg
from tk import *
from tkinter.ttk import Notebook
from WeFunc import *

import requests


class OrderPlacer(tk.Tk):
    def __init__(self):
        # inputs ticker, Nstocks, start, slider for w; % range
        super().__init__()

        self.title("Order Book v1")
        self.notebook = Notebook(self)

        b_tab = tk.Frame(self.notebook)
        o_tab = tk.Frame(self.notebook)
        
        self.ticker = T_field(b_tab, 'Symbol', var_t='str')

        # self.tick_check

        self.Nstocks = T_field(b_tab, 'Quantity')
        self.lo = T_field(b_tab, "Favored")
        self.hi = T_field(b_tab, "Stop")
        self.Nlevels = S_field(b_tab, "Levels", 3, 5, 20)
        self.w = S_field(b_tab, "Scaling", .1, .9, 3, .1)

        self.bb = tk.Button(b_tab, text="Confirm Order", 
                            command=lambda: self.action('c'))
        self.bb.pack(side=tk.BOTTOM, anchor=tk.S)

        self.pb = tk.Button(b_tab, text="Preview Order",
                            command=lambda: self.action('p'))
        self.pb.pack(side=tk.BOTTOM, anchor=tk.S)

        self.pb = tk.Button(o_tab, text="Login",
                            command=lambda: self.action('l'))
        self.pb.pack(side=tk.BOTTOM, anchor=tk.S)

        self.notebook.add(b_tab, text="Buy/Sell Order")
        self.notebook.add(o_tab, text="Options")
        self.notebook.pack(fill=tk.BOTH, expand=1)
    
    def action(self, t=None):
            if t == 'l': #login
                #in wefunc
                getuser()
            l = [self.Nstocks.var.get(), self.hi.var.get(), self.lo.var.get(),
            self.Nlevels.var.get(), self.w.var.get(), self.ticker.var.get()]
            l.reverse()
            print(self.ticker.var.get())
            if t == 'p': #preview
                spread_order(l.pop(), l.pop(), l.pop(), l.pop(), l.pop())
            elif t=='c': #confirm order
                spread_order(l.pop(), l.pop(), l.pop(), l.pop(), l.pop(), l.pop())


class T_field():
    def __init__(self, parent, text, var_t='int'):
        self.parent=parent
        if var_t == 'str':
            self.var = tk.StringVar()
        else:
            self.var = tk.DoubleVar()
            self.var.set(1)
        self.frame = tk.Frame(parent)

        self.label = tk.Label(self.frame, text=text, relief='raised')
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.frame, textvariable=self.var)
        self.entry.pack(side=tk.RIGHT)
        self.frame.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)


class S_field():
    def __init__(self, parent, text, st, default, sp, w=1):
        self.parent = parent
        self.frame = tk.Frame(parent)

        self.label = tk.Label(self.frame, text=text, relief='raised')
        self.label.pack(side=tk.LEFT)

        self.var = tk.Scale(self.frame, from_=st, to=sp, showvalue=0,
                              orient=tk.HORIZONTAL, resolution=w)

        self.label = tk.Label(self.frame, text=self.var.get(), relief='raised')
        self.label.pack(side=tk.RIGHT)
        self.var.set(default)
        self.label.after(200,self.update_label)

        self.var.pack(side=tk.RIGHT)
        self.frame.pack(side=tk.TOP, anchor=tk.NW,fill=tk.X)
    
    def update_label(self):
        self.label.config(text=self.var.get())
        self.label.after(200, self.update_label)

if __name__ == "__main__":
    OrderPlacer = OrderPlacer()
    OrderPlacer.mainloop()