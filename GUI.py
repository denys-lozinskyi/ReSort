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

logo = Label(window, text="ReSort", bg="#f9f9f6", font=("Brush Script MT", 32))
logo.place(x=40, y=5)

display1 = Text(window, width=60, height=30, spacing3 = 2, font=("Timesnewroman", 10))
display1.place(x=300, y=80)

display2 = Text(window, width=60, height=30, spacing3 = 2, font=("Timesnewroman", 10))
display2.place(x=850, y=80)

display1.insert(END, "Bring yourself online, Dolores")

arrow = Label(window, text="⇒", bg="#f9f9f6", font=("Times New Roman", 32))
arrow.place(x=760, y=310)

button_source = Button(window,text="Выберите папку для анализа", padx="20", pady="20", command=None)
button_source.place(x=40, y=80)

button_dest = Button(window,text="Выберите папку назначения", padx="20", pady="20", command=None)
button_dest.place(x=40, y=160)

move_but = Radiobutton(window, text="Переместить", bg="#f9f9f6")
copy_but = Radiobutton(window, text="Только копировать", bg="#f9f9f6")
move_but.place(x=50, y=240)
copy_but.place(x=50, y=270)

button_start = Button(window, text="Начать", padx="20", pady="20", command=None)
button_start.place(x=95, y=320)

button_jumptosource = Button(window,text="Перейти", padx="20", pady="10")
button_jumptosource.place(x=460, y=650)

button_jumptodest = Button(window,text="Перейти", padx="20", pady="10")
button_jumptodest.place(x=1010, y=650)


window.mainloop()
