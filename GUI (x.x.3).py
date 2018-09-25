####################
#     GUI x.x.3    #
####################

from tkinter import *
from tkinter import filedialog

def source_folder():
    global PATH2SOURCE_FOLDER
    PATH2SOURCE_FOLDER = (filedialog.askdirectory(title = "Выберите папку с файлами") + "/")
    if PATH2SOURCE_FOLDER == "/":
        return
    else:
        status.config(text=("***** Папка для анализа:    " + PATH2SOURCE_FOLDER))

def dest_folder():
    global PATH2DEST_FOLDER
    PATH2DEST_FOLDER = (filedialog.askdirectory(title = "Выберите папку с файлами") + "/")
    if PATH2DEST_FOLDER == "/":
        return
    else:
        status.config(text=("***** Папка для перемещения/копирования:    " + PATH2DEST_FOLDER))

def lp():
    #функция исключительно для тестирования вывода
    for a in range(100):
        display1.insert(END, (str(a) + " Bring yourself online, Dolores"))
        display2.insert(END, (str(a) + " I am in a dream"))
        window.update_idletasks()

def BothScroll(*args):
    #обеспечивает одновременный скроллинг листбоксов одним скроллером
    display1.yview(*args)
    display2.yview(*args)
    
def jumptosource():
    try:
        os.startfile(PATH2SOURCE_FOLDER)
    except:
        status.config(text="***** Вы не выбрали папку для анализа")
        
def jumptodest():                      
    try:
        os.startfile(PATH2DEST_FOLDER)
    except:
        status.config(text="***** Вы не выбрали папку назначения")

def info():
    pass

def BothScroll(*args):
    #обеспечивает одновременный скроллинг листбоксов одним скроллером
    display1.yview(*args)
    display2.yview(*args)
        

window = Tk()
general_bg ="#BDBDBD" #цвет общего фона
displays_bg = "#F5F6CE" #цвет фона дисплеев
window.title("ReSort build 2.0.3 beta")
window.geometry("1366x768")
window.configure(bg=general_bg)

logo = Label(window, text="ReSort", bg=general_bg, font=("Brush Script MT", 32))
logo.place(x=40, y=5)
info = Label(window, text="Reference Sorting Tool", bg=general_bg, font=("Times New Roman", 8, "italic"))
info.place(x=80, y=50)

scrollbar = Scrollbar(window, orient="vertical", command=BothScroll)
scrollbar.pack(side=RIGHT, fill=Y)

display1 = Listbox(window, width=55, height=25, bd=2, bg=displays_bg, font=("Times New Roman", 12), yscrollcommand=scrollbar.set)
display1.place(x=300, y=85)

display2 = Listbox(window, width=55, height=25, bd=2, bg=displays_bg, font=("Times New Roman", 12), yscrollcommand=scrollbar.set)
display2.place(x=830, y=85)

arrow = Label(window, text="⇒", bg=general_bg, font=("Times New Roman", 32))
arrow.place(x=765, y=325)

button_source = Button(window,text="Выберите папку для анализа", padx="15", pady="20", relief=RIDGE, command=source_folder)
button_source.place(x=40, y=85)

button_dest = Button(window,text="Выберите папку назначения", padx="16", pady="20", relief=RIDGE, command=dest_folder)
button_dest.place(x=40, y=165)

var=IntVar()
var.set(0)
move_but = Radiobutton(window, text="Переместить", bg=general_bg, variable=var, value=0)
copy_but = Radiobutton(window, text="Только копировать", bg=general_bg, variable=var, value=1)
move_but.place(x=50, y=245)
copy_but.place(x=50, y=275)

button_start = Button(window, text="Начать", padx="20", pady="20", relief=RIDGE, command=lp) #ReSort
button_start.place(x=95, y=325)

button_jumptosource = Button(window,text="Перейти", padx="50", pady="10", relief=RIDGE, command=jumptosource)
button_jumptosource.place(x=445, y=605)

button_jumptodest = Button(window,text="Перейти", padx="50", pady="10", relief=RIDGE, command=jumptodest)
button_jumptodest.place(x=1000, y=605)

status = Label(window, text="***** Добро пожаловать в ReSort! Где будем искать файлы?", bd=5, bg="#E6E6E6", anchor=W)
status.pack(side=BOTTOM, fill=X)

info_button = Button(window, text="Info", font=("Brush Script MT", 26), width=5, height=1, bg=general_bg, relief=FLAT, activebackground=general_bg, command=info)
info_button.pack(side=TOP, anchor=E)

#progress = ttk.Progressbar(status, orient="horizontal", length=191, mode="determinate")
#progress.pack(side=BOTTOM, anchor=E)

window.mainloop()
