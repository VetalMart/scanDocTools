import os
import shutil
import pickle
import csv
import logging

logging.basicConfig(filename='programInfo.txt', level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(messages)s')


"""
#рабочие адреса папок 
dirWithPickleFile = input("папка (окружения) с файлом pickle> ")
dirWithScanFiles = input("папка с отсканированными файлами> ")
intermidiateDir = input("папка для переименованых папок с файлами> ")
dirDestination = input("корневая папка, с районами> ")
"""
# стандратное имя файла
akt = 'акт прийняття внурішніх і зовнішніх мереж.pdf'

# задаем адрес папки окружения
# os.chdir('c:\\users\\vitalii.martynenko\\python\\')
# os.chdir(dirWithPickleFile)


def packInPickle():
    """
    функция для создания списка который будет упакован в pickle
    возвращает список имен
    """
    totalZayavkaList = []
    while True:
        a = input("номер/журнал заявка/программа заявка/ФИО> ").split(' ')
        totalZayavkaList.append(a)
        if a == ['1']:
            break

    totalZayavkaList.pop()
    return totalZayavkaList


def createFilePickle(source, name):
    """
    функция для упакования имен в файл pickle
    на входе список source с информацией для упаковки
    name - имя файла pickle
    """
    with open('{0}.pickle'.format(name), 'wb') as handle:
        pickle.dump(source, handle, protocol=pickle.HIGHEST_PROTOCOL)


def getInformationFromPickleFile(source):
    """
    функция для чтения файла pickle
    возвращает список с информацией
    source - файл pickle с информацией
    """
    with open(source, 'rb') as handle:
        data = pickle.load(handle)
    return data

def getInfoFromTxtFile(source):
    """
    функция которая импортирует данные с txt файла
    возвращает список с данными
    """
    with open(source, 'r') as txtfile:
        data = [' '.join(i.rstrip('\n').split(' ')[1:]) for i in txtfile]
        return data


def nameClean(source):
    """
    !!!!!!!!!!!!for PICKLE files !!!!!!!!!!!!!!!!!!
    
    функция для создания чистых имен
    на входе список source с информацией
    возвращает список с именами для папок
    """
    fileNamesClean = ['{0} {1} {2}'.format(i[2], i[3], i[4]) for i in source]
    return fileNamesClean

def nameCleanCSV(source):
    """
    !!!!!!!!!!!!for CSV files!!!!!!!!!!!!!!!!!!!!!!

    функция для создания чистых имен
    на входе список source с информацией
    возвращает список с именами для папок
    """
    fileNamesClean = ['{0} {1}'.format(i[0], i[1]) for i in source]
    return fileNamesClean

def namePdf(source):
    """
    функция для создания имен с окончанием .pdf
    на входе список source с функиции nameClean
    возвращает список с именами для файлов с расширением .pdf
    """
    fileNamesPdf = ['{0}.pdf'.format(i) for i in source]
    return fileNamesPdf


def renameFiles(sourceDir, pdfNameList):
    """
    функция которая переименовывает скан-копии в файлы 
    с номером с программы заявка, фамилией и инициалами,
    и с расширением pdf
    на вход ей нужно:
    1. sourceDir - адрес с файлами (переменная dirWithScanFiles)
    2. pdfNameList - список с именами файлов с расширением pdf 
            (результат функции namePdf)

    задаем нулевой счетчик counter
    """
    counter = 0
    # входим в папку со сканами
    os.chdir(sourceDir)
    for i in os.listdir():
        # проходимся по папке со сканами, и по списку с именами
        # по ходу присваивая их каждому файлу
        os.rename(i, pdfNameList[counter])
        # увеличиваем счетчик на 1 - переходя к следующей паре "файл/имя"
        counter += 1


def createIntermidiateDir(imd, dwsf, nCl):
    """
    функция которая должна:
    1. создать папки
    2. забросить туда файлы
    3. переименовать их в нужную форму
    imd - папка для хранения уже переименованых папок с файлами
    (переменная intermidiateDir)
    dwcf - папка со сканироваными файлами 
    так же нужен счетчик counter для прохождения по списку: 
    самих файлов dwcf переменная dirWithScanFiles, 
    имен папок список nCl (результат nameClean), 

    что бы понять количество файлов, которые нужно разбросать по 
    папкам,-нужно находиться в папке со сканами dwsf-
    """
    counter = 0
    for i in os.listdir(dwsf):
        # адрес папки которая будет создана
        newDir = '{0}\\{1}'.format(imd, nCl[counter].rstrip())
        # создаем папки с нужными именами в промежуточной папке!
        os.mkdir(newDir)
        # тепер в только что созданную папку, нужно переместить файл
        print('1:', "{0}\\{1}".format(dwsf, i))
        print('2:', "{0}\\{1}".format(newDir, i))
        shutil.copy("{0}\\{1}".format(dwsf, i),
                    '{0}\\{1}'.format(newDir, i))
        # теперь перемещенный файл нужно переименовать в стандартную форму
        os.rename('{0}\\{1}'.format(newDir, i),
                  '{0}\\{1}'.format(newDir, akt))
        # увеличиваем счетчик на 1 и переходим к следующим парам
        counter += 1


def replaceByRegion(imd, dD):
    """
    проверочно-перемещательная функция.
    1. переместиться в нужное окружение - папку с переименоваными 
    файлами
    2. проходом for сначала прочесать свою папку, потом сетевую
    с районами и найти нужный нам район.
    3. проходом for по папке с районом и если есть нужная - то 
    заходим в нее, если нет - создаем;  
    4. если нашлось и совпали - копируем только файл с исходной
    5. если не нашлось в сетевой папке совпадения - копируем всю папку
    
    lFolders = []
    lFiles = []
    lPass = []
    """
    def checkRegion(iter1, iter2, str1, str2, name, folderD, folderS):
        """
        iter1-имя папка объектa в промежуточной папки
        iter2-имя папка района в сетевой папке
        str1-код района нормальный
        str2-дибильный код района в сетевой папке
        name-глобальная переменная - конечное имя акта
        folderD-конечная сетевая папка, в которой осуществляется поиск 
                папки района
        folderS-промежуточная папка, с папками абонентов и файлами внутри
        ее прототип дальше в коментах, как что и куда
        """
        # проверка региона
        if (iter1.startswith(str(str1))
                and iter2.startswith(str(str2))):
            # переходим в нужную папку района и проходим по ней
            # заходим в нужный нам район сетевой папки
            # проверка полного совпадения имени папки
            if os.path.isdir('{0}\\{1}\\{2}'.format(
                    folderD, iter2, iter1)):
                # если да - проверка совпадения файла
                if os.path.isfile('{0}\\{1}\\{2}\\{3}'.format(
                        folderD, iter2, iter1, name)):
                    # если да - сматываем удочки

                    logging.info('{0}\\{1}\\{2}\\{3} - этот файл \
                        уже существовал;'.format(folderD, iter2, iter1, name))
                    #lPass.append('{0}\\{1}\\{2}\\{3}'.format(
                    #    folderD, iter2, iter1, name))
                    pass
                else:
                    # если нет - копируем файл в папку
                    shutil.copy('{0}\\{1}\\{2}'.
                                format(folderS, iter1, name),
                                '{0}\\{1}\\{2}\\{3}'.format(
                                    folderD, iter2, iter1, name))
                    logging.info('папка - {0}\\{1}\\{2} существовала, \
                        файл - {3} добавили;'.format(
                        folderD, iter2, iter1, name))
                    #lFiles.append('{0}\\{1}\\{2}\\{3}'.format(
                    #    folderD, iter2, iter1, name))
            else:
                os.chdir('{0}\\{1}'.format(folderD, iter2))
                # если полного совпадения имени папки нет - делаем
                # проверку совпадения частичного имени папки [0:9]
                for k in os.listdir():
                    # проверяем частичные совпадения по коду программы заявка
                    if (k[0:9] == iter1[0:9]):
                        # если да - копируем файл
                        shutil.copy('{0}\\{1}\\{2}'.
                                    format(folderS, iter1, name),
                                    '{0}\\{1}\\{2}\\{3}'.format(
                                        folderD, iter2, k, name))
                        logging.info('папка - {0}\\{1}\\{2} совпала по номеру \
                            с программы заявка, файл - {3} добавили;'.format(
                            folderD, iter2, k, name))
                        #lFiles.append('{0}\\{1}\\{2}\\{3}'.format(
                        #    folderD, iter2, k, name))
                        break
                else:
                    # если нет - копируем в корневую папку все дерево
                    shutil.copytree('{0}\\{1}'.format(folderS, iter1),
                                    '{0}'.format(iter1))
                    logging.info('создали каталок с файлом -{0}\\{1}\\{2}\
                        \\{3}'.format(folderD, iter2, iter1, name))
                    #lFolders.append('{0}\\{1}\\{2}\\{3}'.format(
                    #    folderD, iter2, iter1, name))

    # проходим по папке с переименоваными папками
    for i in os.listdir(imd):
        """
        проходим по корневой сетевой папке с районами
        dD = dirDestination и если находим подходящий район
        заходим в эту папку, и делаем проверку на наличе подходящей 
        папки объекта. Если есть - то копируем в нее только файл, 
        если нет - то копируем всю папку с файлом 
        """
        for j in os.listdir(dD):
            if not j.endswith(' - Ярлык.lnk'):
                checkRegion(i, j, '25.', '17_', akt, dD, imd)
                checkRegion(i, j, '06.', '05_', akt, dD, imd)
                checkRegion(i, j, '23.', '07_', akt, dD, imd)
                checkRegion(i, j, '11.', '18_', akt, dD, imd)
    """
    # создание лог файла
    print('\nсписок папок которые были созданы:\n ')
    for i in lFolders:
        print(i)

    print('\nсписок файлов которые были созданы:\n ')
    for i in lFiles:
        print(i)

    os.chdir(imd)
    print('''\n\nна рабочем столе у вас создаться файл с именем
        listAdded.txt - там список файлов и папок которые
        были добавлени в сетевую папку''')
    with open('c:\\users\\{0}\\desktop\\listAdded.txt'.format(
            os.getlogin()), 'w', encoding='utf-8') as file:
        print('список папок которые были созданы:\n ',
              file=file, sep='\n')
        print(*enumerate(lFolders, start=1), file=file, sep='\n')
        print('список файлов которые были созданы:\n ',
              file=file, sep='\n')
        print(*enumerate(lFiles, start=1), file=file, sep='\n')
        print('\nсписок пропущених файлов:\n ',
              file=file, sep='\n')
        print(*enumerate(lPass, start=1), file=file, sep='\n')
    """