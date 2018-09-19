####################
#       GUI        #
####################

from tkinter import *
from tkinter import filedialog

def source_folder():
    window.directory = filedialog.askdirectory(initialdir = "/",title = "Выберите папку с файлами")
    return window.directory

def dest_folder():
    window.directory = filedialog.askdirectory(initialdir = "/",title = "Выберите папку с файлами")
    return window.directory

window=Tk()
window.geometry("1000x600")
window.title("ReSort")

button_source=Button(window,text="Выберите папку для анализа", padx="20", pady="20", command=source_folder)
button_source.place(x=40, y=50)

button_dest=Button(window,text="Выберите папку назначения", padx="20", pady="20", command=dest_folder)
button_dest.place(x=40, y=130)

display=Text(window, width=125, height=35)
display.place(x=300, y=45)

button_start=Button(window, text="Начать", padx="20", pady="20")
button_start.place(x=95, y=230)

scroll=Scrollbar(command=display.yview)
scroll.pack(side=RIGHT, fill=Y)
display.config(yscrollcommand=scroll.set)

#display.insert(END, "Hello")


window.mainloop()


