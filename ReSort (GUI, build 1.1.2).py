#-------------------------------------------------------------------------------
# Name:        ReSort
# Author:      Denys Lozinskyi
# Version:     v. 1.0.2 (GUI)
# ------------------------------------------------------------------------------

import os, re, zipfile
from shutil import move
from xml.etree.ElementTree import XML
from tkinter import *
from tkinter import filedialog


def get_docx_text(path):
    """Модуль извлекает текст из MS XML Word document (.docx) и превращает его строку в формате Unicode.
       Разработчик ядра модуля: Etienne, http://etienned.github.io/posts/extract-text-from-word-docx-simply/
       Адаптировано для парсинга по docx и ReSort: Денис Лозинский
    """
    #ниже - переменные, необходимые для docx парсинга, поскольку файлы docx представляют из себя заархивированные namespaced XML
    word_namespace = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    para = word_namespace + 'p'
    text = word_namespace + 't'

    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)    

    paragraphs = []
    for paragraph in tree.iter(para):
        texts = [node.text for node in paragraph.iter(text) if node.text]        
        if texts:
            paragraphs.append(''.join(texts))
    joint_text = ' '.join(paragraphs)
    
    result_list = re.findall(r'\w+', joint_text) #на выходе имеем список слов без пробелов в формате юникод
    result_str = ' '.join(result_list) #на выходе имеем текст в виде строки без знаков пунктуации

    return result_str


def is_dpk(file):
    '''функция проверяет, является ли file типом ДПК. Слова-маркеры разделены на группы.
       Файл ДПК отличает то, что в нем присутствуют слова из каждой из указанных групп.
       Группы маркеров можно добавлять, если необходимо
    '''
    
    markers = (("справка", "reference", "βεβαιωσις"),
               ("каноничным", "canonically", "κανονικώς"),
               ("клириком", "clergyman", "χειροτονημένος"),
               ("священнодействовать", "ministering", "ιεροπράττει"),
               ("церкви", "church", "εκκλησίας"))

    for i in range(len(markers)):
        control = 0
        for j in range(len(markers[i])):
            if markers[i][j] in file:
                #print(markers[i][j])
                control += 1
        #print(control)
        '''control увеличивается на единицу при совпадении слов с каждым отдельным вложенным кортежем,
           что обуславливает продолжение итерации верхнего уровня, и обнуляется при каждом переходе к следующему вложенному кортежу.
           Таким образом, несовпадение с хотя бы одним из вложенных кортежей делает control равным нулю и возвращает False.
           Если с каждым из кортежей совпадение есть, возвращаем True
        '''
        if control == 0:
            return False
    return True

def title_maker(file):
    '''функция принимает файл дпк, находит в нем имя и фамилию того, кому выдана справка,
       и возвращает строку в формате Имя Фамилия, о каноничности.docx
       Если в целевой папке имя уже присутствует, возвращает (с помощью if_dublicate_title) имя и фамилию в формате:
       Михаил Васнецов(n).docx. Если имя в файле найти не удалось, возвращает default_name(n).docx
    '''
    
    default_name = 'справка о каноничности.docx'
    file_content = file.split()
    #print(file_content)    
    for i in range(len(file_content)):
        #print(file_content[i])
        
        if file_content[i] == 'свидетельствуем':
            name = str(file_content[i+3])
            if file_content[i+5] == 'миру':
                surname = str(file_content[i+7])
            else:
                surname = str(file_content[i+4])
        elif file_content[i] == 'certify':
            name = str(file_content[i+3])
            if file_content[i+5] == 'name':
                surname = str(file_content[i+7])
            else:
                surname = str(file_content[i+4])
        elif file_content[i] == 'βεβαίωσιν':
            name = str(file_content[i+2])
            if file_content[i+4] == 'κόσμον':
                surname = str(file_content[i+6])
            else:
                surname = str(file_content[i+3])        
    try:                    
        title = name.capitalize() + ' ' + surname.capitalize() + ', о каноничности.docx'
        #print(title)
        #print(os.listdir(PATH2DEST_FOLDER))
    except:
        '''если имя и фамилию определить не удалось (слова-маркеры для индексации фамилии и имени отсутствуют
           или написаны с ошибками), установить имя по умолчанию. Потом проверить, есть ли файл с таким именем в папке
        '''
        title = default_name
    if title in os.listdir(PATH2DEST_FOLDER):
        return if_dublicate_title(title)
    else:
        display2.insert(END, title)
        display2.yview(END) #следить за скроллом, при необходимости - удалить
        window.update_idletasks()
        return title

        
def if_dublicate_title(file_name):
    '''функция вызывается из title_maker в случае, если файл с таким именем уже присутствует в папке назначения.
       Функция возвращает принимаемое имя файла с его расширением в формате ИМЯ(n).расширение,
       где n - нумератор повторений имени файла, целое число, начиная с 2,
       соответствующее количеству повторений имени файла в папке
    '''
    
    title_constructor = file_name.split('.') #отделяем имя файла от расширения, попутно образовывая список
    title_constructor.append(1) #добавляем в список нумератор повторений
    #print(title_constructor)
    while file_name in os.listdir(PATH2DEST_FOLDER): #до тех пор, пока файл с таким именем присутствует в папке
        title_constructor[2] += 1 #увеличиваем нумератор на единицу
        file_name = ('%s' + '(%s).' + '%s') %(title_constructor[0], title_constructor[2], title_constructor[1]) #собираем новое имя файла и снова отдаем его на проверку
    display2.insert(END, file_name)
    display2.yview(END) #следить за скроллом, при необходимости - удалить
    window.update_idletasks()
    return file_name


def ReSort():
    """на этом месте сделать полноценную проверку путей. Исключение ниже обрабатывает только наличие пути к исходной папке
       но нужно проверить и папку назначения, чтобы не скопировало файлы куда попало
    """   
    try:
        files_to_scan = os.listdir(PATH2SOURCE_FOLDER)
    except:
        status.config(text="Сначала выберите папку для анализа")
        return

    #print('Файлы ДПК:') #вводная фраза, пока что в консоль, потом переназначить в Label

    #сканируем каждый файл из списка
    dpk_count = 0
    status.config(text=("Обработка..."))
    for document in files_to_scan:
        if document[-5:] == ".docx":            
            #print(document)
            file = get_docx_text(PATH2SOURCE_FOLDER + document)
            file = file.lower()    
            #print(file)
            if is_dpk(file):
                dpk_count += 1
                display1.insert(END, document)
                display1.yview(END) #следить за скроллом, при необходимости - удалить
                window.update_idletasks() #необходим, чтобы строки выводились по мере выполнения программы, а не все сразу в конце
                move(PATH2SOURCE_FOLDER + document, PATH2DEST_FOLDER + title_maker(file)) #перемещение файла в папку с переименованием                
            '''перемеименование лучше совместить с перемещением (благо, shutil.move это позволяет, т.к. сам использует os.rename)
               поскольку если перед перещением в папке назначения уже будет присутствовать файл с таким же именем,
               move сгенерирует ошибку. Обезопаситься от ошибки можно только перемещением файла с уникальным именем.
               Эту уникальность обеспечит title_maker, работающий совместно с if_dublicate_title
            '''
            #else:
                #print(document + ' - не ДПК')
    if dpk_count == 0:
        status.config(text="В выбранной папке файлы ДПК отсутствуют")
    else:
        status.config(text=("Было обнаружено и перенесено " + str(dpk_count) + " ДПК"))

def source_folder():
    global PATH2SOURCE_FOLDER
    PATH2SOURCE_FOLDER = (filedialog.askdirectory(title = "Выберите папку с файлами") + "/")
    status.config(text=("Папка для анализа:    " + PATH2SOURCE_FOLDER))

def dest_folder():
    global PATH2DEST_FOLDER
    PATH2DEST_FOLDER = (filedialog.askdirectory(title = "Выберите папку с файлами") + "/")
    status.config(text=("Папка для перемещения/копирования:    " + PATH2DEST_FOLDER))

def jumptosource():
    try:
        os.startfile(PATH2SOURCE_FOLDER)
    except:
        status.config(text="Вы не выбрали папку для анализа")
        

def jumptodest():                      
    try:
        os.startfile(PATH2DEST_FOLDER)
    except:
        status.config(text="Вы не выбрали папку назначения")

def BothScroll(*args):
    #обеспечивает одновременный скроллинг листбоксов одним скроллером
    display1.yview(*args)
    display2.yview(*args)
    
    

window = Tk()
general_bg ="#BDBDBD" #цвет общего фона
displays_bg = "#F5F6CE" #цвет фона дисплеев
window.title("ReSort build 1.0.2 alpha")
window.geometry("1000x600")
window.configure(bg=general_bg)


logo = Label(window, text="ReSort", bg=general_bg, font=("Brush Script MT", 32))
logo.place(x=40, y=5)

scrollbar = Scrollbar(window, orient="vertical", command=BothScroll)
scrollbar.pack(side=RIGHT, fill=Y)

display1 = Listbox(window, width=55, height=25, bd=2, bg=displays_bg, font=("Times New Roman", 12), yscrollcommand=scrollbar.set)
display1.place(x=300, y=80)

display2 = Listbox(window, width=55, height=25, bd=2, bg=displays_bg, font=("Times New Roman", 12), yscrollcommand=scrollbar.set)
display2.place(x=850, y=80)

arrow = Label(window, text="⇒", bg=general_bg, font=("Times New Roman", 32))
arrow.place(x=775, y=310)

button_source = Button(window,text="Выберите папку для анализа", padx="20", pady="20", command=source_folder)
button_source.place(x=40, y=80)

button_dest = Button(window,text="Выберите папку назначения", padx="20", pady="20", command=dest_folder)
button_dest.place(x=40, y=160)

move_but = Radiobutton(window, text="Переместить", bg=general_bg)
copy_but = Radiobutton(window, text="Только копировать", bg=general_bg)
move_but.place(x=50, y=240)
copy_but.place(x=50, y=270)

button_start = Button(window, text="Начать", padx="20", pady="20", command=ReSort)
button_start.place(x=95, y=320)

button_jumptosource = Button(window,text="Перейти", padx="20", pady="10", command=jumptosource)
button_jumptosource.place(x=470, y=600)

button_jumptodest = Button(window,text="Перейти", padx="20", pady="10", command=jumptodest)
button_jumptodest.place(x=1025, y=600)

status = Label(window, text="Добро пожаловать в ReSort! Где будем искать файлы?", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

window.mainloop()
