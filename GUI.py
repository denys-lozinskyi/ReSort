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
    for a in range(100):
        display1.insert(END, (str(a) + " Bring yourself online, Dolores"))
        display2.insert(END, (str(a) + " I am in a dream"))

def BothScroll(*args):
    #для одновременного скроллинга двух listboxes
    display1.yview(*args)
    display2.yview(*args)
       

window = Tk()
bg_colour="#BDBDBD" #цвет фона
window.title("ReSort")
window.geometry("1000x600")
window.configure(bg=bg_colour)


logo = Label(window, text="ReSort", bg=bg_colour, font=("Brush Script MT", 32))
logo.place(x=40, y=5)

scrollbar = Scrollbar(window, orient="vertical", command=BothScroll)
scrollbar.pack(side=RIGHT, fill=Y)

display1 = Listbox(window, width=55, height=25, bd=2, bg="#F5F6CE", font=("Times New Roman", 12), yscrollcommand=scrollbar.set)
display1.place(x=300, y=80)

display2 = Listbox(window, width=55, height=25, bd=2, bg="#F5F6CE", font=("Times New Roman", 12), yscrollcommand=scrollbar.set)
display2.place(x=850, y=80)

arrow = Label(window, text="⇒", bg=bg_colour, font=("Times New Roman", 32))
arrow.place(x=775, y=310)

button_source = Button(window,text="Выберите папку для анализа", padx="20", pady="20", command=source_folder)
button_source.place(x=40, y=80)

button_dest = Button(window,text="Выберите папку назначения", padx="20", pady="20", command=dest_folder)
button_dest.place(x=40, y=160)

move_but = Radiobutton(window, text="Переместить", bg=bg_colour)
copy_but = Radiobutton(window, text="Только копировать", bg=bg_colour)
move_but.place(x=50, y=240)
copy_but.place(x=50, y=270)

button_start = Button(window, text="Начать", padx="20", pady="20", command=ReSort)
button_start.place(x=95, y=320)

button_jumptosource = Button(window,text="Перейти", padx="20", pady="10")
button_jumptosource.place(x=470, y=600)

button_jumptodest = Button(window,text="Перейти", padx="20", pady="10")
button_jumptodest.place(x=1025, y=600)


window.mainloop()

