from tkinter import *

def donothing():
    i = 0

# Setup application window
mainWindow = Tk()
mainWindow.title('SoundSight')

mainWindow.geometry("1280x720")
mainWindow.config(background = "black")

# Create menu bar
menubar = Menu(mainWindow)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu = filemenu)

filemenu.add_command(label="Open File", command=donothing)
filemenu.add_command(label="Open Directory", command=donothing)
filemenu.add_command(label="Close File", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=mainWindow.quit)

mainWindow.config(menu = menubar)

mainWindow.mainloop()