####################
#       GUI        #
####################

from tkinter import *
from tkinter import filedialog

def source_folder():
    global PATH2SOURCE_FOLDER
    PATH2SOURCE_FOLDER = (filedialog.askdirectory(initialdir = "\\", title = "Выберите папку с файлами") + "\\")  

def dest_folder():
    global PATH2DEST_FOLDER
    PATH2DEST_FOLDER = (filedialog.askdirectory(initialdir = "\\", title = "Выберите папку с файлами") + "\\")

window = Tk()
window.title("ReSort")
window.geometry("1000x600")
window.configure(bg="#f9f9f6")

display1 = Text(window, width=60, height=30, spacing3 = 2, font=("Timesnewroman", 10))
display1.place(x=300, y=50)

display2 = Text(window, width=60, height=30, spacing3 = 2, font=("Timesnewroman", 10))
display2.place(x=850, y=50)

arrow = Label(window, text="⇒", bg="#f9f9f6", font=("Times New Roman", 32))
arrow.place(x=760, y=300)

button_source = Button(window,text="Выберите папку для анализа", padx="20", pady="20", command=source_folder)
button_source.place(x=40, y=50)

button_dest = Button(window,text="Выберите папку назначения", padx="20", pady="20", command=dest_folder)
button_dest.place(x=40, y=130)

button_start = Button(window, text="Начать", padx="20", pady="20", command=ReSort)
button_start.place(x=95, y=230)

button_jumptosource = Button(window,text="Перейти", padx="20", pady="10")
button_jumptosource.place(x=460, y=620)

button_jumptodest = Button(window,text="Перейти", padx="20", pady="10")
button_jumptodest.place(x=1010, y=620)


window.mainloop()
