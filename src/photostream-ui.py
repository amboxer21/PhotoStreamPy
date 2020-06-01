#!/usr/bin/env python

import tkinter as tk

from tkinter import messagebox

class PhotstreamUI(object):

    def __init__(self):

        self.tk = tk.Tk()

        self.tk.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
        self.tk.title("PhotstreamUI")


        canvas = tk.Canvas(self.tk, bg="white", width=500, height=300)
        canvas.pack(side="top", fill="both", expand=True)
        #cid = canvas.create_text(10, 10, anchor="nw")
        #canvas.itemconfig(cid, text="TESTING!")

        download_button = tk.Button(self.tk, text='test', command=self.download_button)
        download_button.pack()

    def download_button(self):
        messagebox.showinfo( "PhotstreamUI", "Downloading your FB photostream now!")

    def menu(self):
        self.tk.mainloop()

if __name__ == '__main__':
    PhotstreamUI().menu()
