#-------------------------------------------------------------------------------
# Name:        ReSort
# Author:      Denys Lozinskyi
# Version:     v.1.0 (Console)
# ------------------------------------------------------------------------------

import os, re, zipfile
from shutil import move
from xml.etree.ElementTree import XML

#задаем пути к папкам (в финальной версии пути будут задаваться пользователем)
PATH2SOURCE_FOLDER = "g:\Python\\file_parsing\source_folder\\"
PATH2DEST_FOLDER = "g:\Python\\file_parsing\ДПК\\"

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
    return file_name


########################
#       MAIN BODY      #
########################

#создаем список файлов в выбранной директории (может задаваться пользователем вручную)
files_to_scan = os.listdir(PATH2SOURCE_FOLDER)

#print('Файлы ДПК:') #вводная фраза для вывода перечня файлов ниже
#сканируем каждый файл из списка
dpk_count = 0
for document in files_to_scan:
    if document[-5:] == ".docx":        
        #print(document)
        file = get_docx_text(PATH2SOURCE_FOLDER + document)
        file = file.lower()    
        #print(file)
        if is_dpk(file):
            dpk_count += 1
            print(document) #для тестирования
            move(PATH2SOURCE_FOLDER + document, PATH2DEST_FOLDER + title_maker(file)) #перемещение файла в папку с переименованием
            '''перемеименование лучше совместить с перемещением (благо, shutil.move это позволяет, т.к. сам использует os.rename)
               поскольку если перед перещением в папке назначения уже будет присутствовать файл с таким же именем,
               move сгенерирует ошибку. Обезопаситься от ошибки можно только перемещением файла с уникальным именем.
               Эту уникальность обеспечит title_maker, работающий совместно с if_dublicate_title
            '''
        #else:
            #print(document + ' - не ДПК')
if dpk_count == 0:
    print("В выбранной папке ДПК отсутствуют")
else:
    print("Было обнаружено ", dpk_count, "ДПК")        
           
