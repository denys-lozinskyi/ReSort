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

def lp():
    #функция для тестирования вывода
    for a in range(30):
        display1.insert(1.0, "Bring yourself online, Dolores\n")

window = Tk()
bg_colour="#BDBDBD" #цвет фона
window.title("ReSort")
window.geometry("1000x600")
window.configure(bg=bg_colour)


logo = Label(window, text="ReSort", bg=bg_colour, font=("Brush Script MT", 32))
logo.place(x=40, y=5)

display1 = Text(window, width=60, height=25, bd=2, spacing3 = 3, font=("Times New Roman", 12))
display1.place(x=300, y=80)

display2 = Text(window, width=60, height=25, bd=2, spacing3 = 3, font=("Times New Roman", 12))
display2.place(x=850, y=80)

arrow = Label(window, text="⇒", bg=bg_colour, font=("Times New Roman", 32))
arrow.place(x=795, y=320)

button_source = Button(window,text="Выберите папку для анализа", padx="20", pady="20", command=None)
button_source.place(x=40, y=80)

button_dest = Button(window,text="Выберите папку назначения", padx="20", pady="20", command=None)
button_dest.place(x=40, y=160)

move_but = Radiobutton(window, text="Переместить", bg=bg_colour)
copy_but = Radiobutton(window, text="Только копировать", bg=bg_colour)
move_but.place(x=50, y=240)
copy_but.place(x=50, y=270)

button_start = Button(window, text="Начать", padx="20", pady="20", command=lp)
button_start.place(x=95, y=320)

button_jumptosource = Button(window,text="Перейти", padx="20", pady="10")
button_jumptosource.place(x=490, y=650)

button_jumptodest = Button(window,text="Перейти", padx="20", pady="10")
button_jumptodest.place(x=1045, y=650)


window.mainloop()

